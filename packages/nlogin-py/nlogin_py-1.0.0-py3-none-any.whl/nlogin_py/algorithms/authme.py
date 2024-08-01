import hashlib
import random
import string

from .algorithm import Algorithm


class AuthMe(Algorithm):
    SALT_LENGTH = 16

    def __init__(self):
        self.CHARS = self._init_char_range()

    def hash(self, password: str) -> str:
        salt = self.generate_salt()
        hashed_password = hashlib.sha256(
            hashlib.sha256(password.encode()).hexdigest().encode() + salt.encode()
        ).hexdigest()
        return f"$SHA${salt}${hashed_password}$AUTHME"

    def verify(self, password: str, hashed_password: str) -> bool:
        parts = hashed_password.split("$")
        if len(parts) not in {4, 5}:
            return False
        salt = parts[2]
        expected_hash = hashlib.sha256(
            hashlib.sha256(password.encode()).hexdigest().encode() + salt.encode()
        ).hexdigest()
        return parts[3] == expected_hash

    def generate_salt(self) -> str:
        """
        Generates a random salt string.

        Returns:
            str: The randomly generated salt.
        """
        return "".join(random.choice(self.CHARS) for _ in range(self.SALT_LENGTH))

    @staticmethod
    def _init_char_range():
        return list(string.digits + "abcdef")
