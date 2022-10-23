from datetime import datetime, timedelta, timezone
from typing import Any, Union
from jose import jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='/api/auth/login'
)

password_enc = CryptContext(schemes=["sha256_crypt"],deprecated="auto")

SECRET_KEY = "djsa0iojdosa"


def jwt_create(sub: Union[Any,str]):
    payload = {
        "exp": datetime.now(tz=timezone.utc) + timedelta(hours=15),
        "sub":str(sub)
        }
    token = jwt.encode(payload,SECRET_KEY,algorithm="HS512")
    return token

def jwt_decode(token: str):
    data = jwt.decode(token,SECRET_KEY,algorithms="HS512")
    return data.get('sub')

    
def password_create(password: str):
    return password_enc.hash(password)
    
def password_verify(password: str, encpass: str):
    return password_enc.verify(password,encpass)
