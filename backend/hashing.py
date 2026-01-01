from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash:
    @staticmethod
    def make(password: str):
        return pwd_cxt.hash(password)

    @staticmethod
    def verify(hashed, plain):
        return pwd_cxt.verify(plain, hashed)
