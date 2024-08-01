import hashlib
import random

from .algorithm import Algorithm


class Sha512(Algorithm):
    SALT_LENGTH = 24

    def __init__(self):
        self.CHARS = "".join(chr(i) for i in range(ord("A"), ord("Z") + 1)) + "".join(
            str(i) for i in range(10)
        )

    def hash(self, password: str) -> str:
        salt = self._generate_salt()
        hashed_password = hashlib.sha512(
            hashlib.sha512(password.encode()).hexdigest().encode() + salt.encode()
        ).hexdigest()
        return f"$SHA512${hashed_password}${salt}"

    def verify(self, password: str, hashed_password: str) -> bool:
        parts = hashed_password.split("$")
        parts_length = len(parts)
        if parts_length == 3:  # old format
            salt_parts = hashed_password.split("@")
            salt = salt_parts[1]
            return (
                f"{parts[2]}@{salt}"
                == hashlib.sha512(
                    hashlib.sha512(password.encode()).hexdigest().encode()
                    + salt.encode()
                ).hexdigest()
            )
        elif parts_length == 4:  # new format
            return (
                parts[2]
                == hashlib.sha512(
                    hashlib.sha512(password.encode()).hexdigest().encode()
                    + parts[3].encode()
                ).hexdigest()
            )
        else:
            raise Exception(
                f"Invalid hash parts length! length={parts_length}, raw={hashed_password}"
            )

    def _generate_salt(self) -> str:
        return "".join(random.choice(self.CHARS) for _ in range(self.SALT_LENGTH))
