import pymysql
from pymysql.err import OperationalError

from .algorithms import AuthMe, Bcrypt, Sha256, Sha512


class Nlogin:
    FETCH_WITH_MOJANG_ID = 1
    FETCH_WITH_BEDROCK_ID = 2
    FETCH_WITH_LAST_NAME = 3

    def __init__(
        self,
        mysql_host: str,
        mysql_user: str,
        mysql_pass: str,
        mysql_database: str,
        using_username_appender: bool,
        table_name: str = "nlogin",
    ):
        """
        Initializes a new instance of the Nlogin class.

        Args:
            mysql_host (str): The MySQL host to connect to.
            mysql_user (str): The MySQL user to authenticate with.
            mysql_pass (str): The MySQL password to authenticate with.
            mysql_database (str): The MySQL database to connect to.
            using_username_appender (bool): Whether to use the username appender.
            table_name (str, optional): The name of the table to use. Defaults to "nlogin".

        Returns:
            None
        """
        self.authme = None
        self.bcrypt = None
        self.sha256 = None
        self.sha512 = None
        self.hashing_algorithm = None
        self.init_algorithm()
        self._mysql_host = mysql_host
        self._mysql_user = mysql_user
        self._mysql_pass = mysql_pass
        self._mysql_database = mysql_database
        self._using_username_appender = using_username_appender
        self._table_name = table_name

    def init_algorithm(self):
        self.authme = AuthMe()
        self.bcrypt = Bcrypt()
        self.sha256 = Sha256()
        self.sha512 = Sha512()
        self.hashing_algorithm = self.bcrypt

    def fetch_user_id(self, search: str, mode: int):
        connection = self.get_connection()
        if connection is None:
            return None

        search = search.strip()

        try:
            with connection.cursor() as cursor:
                if mode == self.FETCH_WITH_MOJANG_ID:
                    cursor.execute(
                        f"SELECT ai FROM {self._table_name} WHERE mojang_id = %s LIMIT 1",
                        (search,),
                    )
                elif mode == self.FETCH_WITH_BEDROCK_ID:
                    cursor.execute(
                        f"SELECT ai FROM {self._table_name} WHERE bedrock_id = %s LIMIT 1",
                        (search,),
                    )
                elif mode == self.FETCH_WITH_LAST_NAME:
                    if self._using_username_appender:
                        cursor.execute(
                            f"SELECT ai FROM {self._table_name} WHERE last_name = %s AND mojang_id IS NULL AND bedrock_id IS NULL LIMIT 1",
                            (search,),
                        )
                    else:
                        cursor.execute(
                            f"SELECT ai FROM {self._table_name} WHERE last_name = %s ORDER BY mojang_id DESC LIMIT 1",
                            (search,),
                        )
                else:
                    raise ValueError("Invalid search mode")

                result = cursor.fetchone()
                return result[0] if result else -1
        finally:
            connection.close()

    def is_user_registered(self, user_id: int) -> bool:
        return self._exists_in_database("ai", str(user_id))

    def is_ip_registered(self, ip: str) -> bool:
        return self._exists_in_database("last_ip", ip)

    def verify_password(self, user_id: int, password: str) -> bool:
        hashed_password = self.get_hashed_password(user_id)
        if not hashed_password:
            return False

        algorithm = self.detect_algorithm(hashed_password)
        if algorithm is None:
            raise ValueError(
                f"Hashing algorithm cannot be determined for user identifier: {user_id}"
            )

        return algorithm.verify(password, hashed_password)

    def change_password(self, user_id: int, password: str) -> bool:
        connection = self.get_connection()
        if connection is None:
            return False

        try:
            with connection.cursor() as cursor:
                pass_hash = self.hashing_algorithm.hash(password)
                cursor.execute(
                    f"UPDATE {self._table_name} SET password = %s WHERE ai = %s LIMIT 1",
                    (pass_hash, user_id),
                )
                connection.commit()
                return cursor.rowcount > 0
        finally:
            connection.close()

    def register(
        self,
        username: str,
        password: str,
        email: str,
        ip: str = "127.0.0.1",
        mojang_id: str = None,
        bedrock_id: str = None,
    ) -> bool:
        """
        Registers a new user in the system.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.
            email (str): The email of the user.
            ip (str, optional): The IP address of the user. Defaults to 127.0.0.1.
            mojang_id (str, optional): The Mojang ID of the user. Defaults to None.
            bedrock_id (str, optional): The Bedrock ID of the user. Defaults to None.

        Returns:
            bool: True if the user was successfully registered, False otherwise.
        """
        connection = self.get_connection()
        if connection is None:
            return False

        if mojang_id and bedrock_id:
            raise ValueError("mojang_id and bedrock_id cannot be both not null!")

        username = username.strip()

        if mojang_id:
            search, mode = mojang_id, self.FETCH_WITH_MOJANG_ID
        elif bedrock_id:
            search, mode = bedrock_id, self.FETCH_WITH_BEDROCK_ID
        else:
            search, mode = username, self.FETCH_WITH_LAST_NAME

        user_id = self.fetch_user_id(search, mode)
        if user_id is None:
            return False

        email = email or ""
        hashed_password = self.hashing_algorithm.hash(password)

        try:
            with connection.cursor() as cursor:
                if user_id < 0:
                    cursor.execute(
                        f"INSERT INTO {self._table_name} (last_name, password, last_ip, mojang_id, bedrock_id, email) "
                        f"VALUES (%s, %s, %s, %s, %s, %s)",
                        (username, hashed_password, ip, mojang_id, bedrock_id, email),
                    )
                elif mojang_id:
                    cursor.execute(
                        f"UPDATE {self._table_name} SET password = %s, last_ip = %s, mojang_id = %s, email = %s WHERE ai = %s LIMIT 1",
                        (hashed_password, ip, mojang_id, email, user_id),
                    )
                elif bedrock_id:
                    cursor.execute(
                        f"UPDATE {self._table_name} SET password = %s, last_ip = %s, bedrock_id = %s, email = %s WHERE ai = %s LIMIT 1",
                        (hashed_password, ip, bedrock_id, email, user_id),
                    )
                else:
                    cursor.execute(
                        f"UPDATE {self._table_name} SET password = %s, last_ip = %s, email = %s WHERE ai = %s LIMIT 1",
                        (hashed_password, ip, email, user_id),
                    )
                connection.commit()
                return cursor.rowcount > 0
        finally:
            connection.close()

    def get_hashed_password(self, user_id: int) -> str | None:
        """
        Retrieves the hashed password for a given user ID.

        Args:
            user_id (int): The ID of the user.

        Returns:
            str: The hashed password associated with the user ID, or None if no password is found.
        """
        connection = self.get_connection()
        if connection is None:
            return None

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    f"SELECT password FROM {self._table_name} WHERE ai = %s LIMIT 1",
                    (user_id,),
                )
                result = cursor.fetchone()
                return result[0] if result else None
        finally:
            connection.close()

    def detect_algorithm(self, hashed_pass: str):
        algo = hashed_pass.split("$")[1].upper() if "$" in hashed_pass else ""
        if algo in ["2", "2A"]:
            return self.bcrypt
        elif algo == "SHA256":
            return self.sha256
        elif algo == "SHA512":
            return self.sha512
        elif algo == "SHA":
            return self.authme
        else:
            return None

    def _exists_in_database(self, column: str, value: str) -> bool:
        connection = self.get_connection()
        if connection is None:
            return False

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    f"SELECT 1 FROM {self._table_name} WHERE {column} = %s LIMIT 1",
                    (value,),
                )
                return cursor.fetchone() is not None
        finally:
            connection.close()

    def get_connection(self):
        try:
            connection = pymysql.connect(
                host=self._mysql_host,
                user=self._mysql_user,
                password=self._mysql_pass,
                database=self._mysql_database,
            )
            return connection
        except OperationalError as e:
            print(f"Could not connect to {self._mysql_database} database. Error: {e}")
            return None
