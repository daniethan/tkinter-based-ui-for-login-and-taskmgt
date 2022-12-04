from .ext import Hash
import config.vars_ as vars_
from config.dbconfig import session
from config import models


def check_credentials(username: str, password: str):
    user = session.query(models.User).filter(models.User.email==username).first()
    if not user:
        return False
    
    vars_.USER = user

    is_verified = Hash.verify_password(
                                plain_password=password,
                                hashed_password=user.password
                                )
    return is_verified


def validate_password(password: str):
    nlow, nup, ndig, nchar, nsp = 0, 0, 0, 0, 0
    if len(password) >= 8:
        for char in password:
            # counting lowercase alphabets
            if char.islower():
                nlow += 1		
            # counting uppercase alphabets
            if char.isupper():
                nup += 1		
            # counting digits
            if char.isdigit():
                ndig+=1		
            # counting the mentioned special characters
            if not char.isalnum():
                nchar += 1	
            #counting number of white spaces
            if char.isspace():
                nsp += 1	
        if False not in (nlow > 0, nup > 0, ndig > 0, nchar > 0, nsp == 0) and sum((nlow, nup, ndig, nchar))==len(password):
            return True
    return False


def lockout():
    #more robust functionality to be added!
    return False


def auth_with_pin(pin: int, trials: bool):
    is_auth = Hash.verify_password(plain_password=pin, hashed_password=vars_.USER.pin)
    if is_auth:
        return True
    elif not trials:
        return None
    return False
        
    