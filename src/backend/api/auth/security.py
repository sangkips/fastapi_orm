from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordHasher():
    """
    @staticmethod ensures that verify password and get password hashed
    doesnt need to be called through instantiating.

    """
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hashed(password):
        return pwd_context.hash(password)
