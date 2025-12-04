import bcrypt

from mini_crm.application.users.interfaces import PasswordHasher


class BcryptPasswordHasher(PasswordHasher):
    """Реализация хеширования паролей с помощью bcrypt"""

    def hash(self, password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed.decode("utf-8")

    def verify(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            hashed_password.encode("utf-8"),
        )
