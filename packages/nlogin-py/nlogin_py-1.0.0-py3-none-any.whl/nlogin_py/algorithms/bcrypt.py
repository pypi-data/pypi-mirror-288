import bcrypt

from .algorithm import Algorithm


class Bcrypt(Algorithm):
    _saltPrefix = "2a"
    _defaultCost = 14
    _saltLength = 22

    def hash(self, password: str, cost: int = None) -> str:
        """
        Hashes the given password using the bcrypt algorithm.

        Args:
            password (str): The plain text password to hash.
            cost (int, optional): The cost factor for the bcrypt hash. Defaults to 14.

        Returns:
            str: The resulting hash.
        """
        if cost is None:
            cost = self._defaultCost

        salt = self.generate_random_salt()
        hash_string = self._generate_hash_string(cost, salt)

        hashed_password = bcrypt.hashpw(password.encode(), hash_string.encode())
        return hashed_password.decode()

    def verify(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode(), hashed_password.encode())

    def generate_random_salt(self) -> str:
        """
        Generate a random base64 encoded salt.

        Returns:
            str: The randomly generated salt.
        """
        salt = bcrypt.gensalt(rounds=self._defaultCost).decode()
        return salt[-self._saltLength :]

    def _generate_hash_string(self, cost: int, salt: str) -> str:
        return f"${self._saltPrefix}${cost:02}${salt}$"
