from datetime import datetime, timedelta, timezone
from typing import Any, Union
from passlib.context import CryptContext
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import true

password_enc = CryptContext(schemes=["sha256_crypt"],deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/usuarios/login"
)

SECRET_KEY = "secret"


def jwt_create(sub: Union[Any,str]):
    payload = {
        "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=15),
        "sub":str(sub)
        }
    token = jwt.encode(payload,SECRET_KEY,algorithm="HS512")
    return token
    
def jwt_validation(token):
    validation = jwt.decode(token,SECRET_KEY,algorithms="HS512")
    if validation:
        return True 
    else:
        return False

def jwt_get_sub(token):
    data = jwt.decode(token,SECRET_KEY,algorithms="HS512")
    return data.get("sub")
    
def password_create(password: str):
    return password_enc.hash(password)
    
def password_verify(password: str, encpass: str):
    return password_enc.verify(password,encpass)
