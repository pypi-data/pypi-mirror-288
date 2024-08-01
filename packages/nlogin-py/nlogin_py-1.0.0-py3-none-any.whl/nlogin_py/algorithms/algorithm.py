from abc import abstractmethod, ABC


class Algorithm(ABC):
    @abstractmethod
    def hash(self, password: str):
        """
        Hashes the given password.

        Args:
            password (str): The plain text password to hash.

        Returns:
            str: The resulting hash.
        """
        raise NotImplementedError

    @abstractmethod
    def verify(self, password: str, hashed_password: str):
        """
        Verify whether the given password matches the hashed password.

        Args:
            password (str): The plain text password to verify.
            hashed_password (str): The hashed password to compare against.

        Returns:
            bool: True if the password matches the hashed password, False otherwise.
        """
        raise NotImplementedError
