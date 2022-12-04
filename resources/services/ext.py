# file contains reusable code that accomplishes some unique important logic
from passlib.context import CryptContext


pswd_ctxt = CryptContext(schemes=['bcrypt'], deprecated="auto")
class Hash:
    @staticmethod
    def encrypt(password: str) -> str:
        return pswd_ctxt.hash(secret=password)
    
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pswd_ctxt.verify(secret=plain_password, hash=hashed_password)