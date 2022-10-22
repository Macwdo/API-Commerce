from datetime import datetime, timedelta, timezone
from typing import Any, Union
from passlib.context import CryptContext
from jose import jwt
from fastapi.security import OAuth2PasswordBearer

password_enc = CryptContext(schemes=["sha256_crypt"],deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/usuarios/login"
)

SECRET_KEY = "secret"


def jwt_create(sub: Union[Any,str]):
    payload = {
        "exp": datetime.now(tz=timezone.utc) + timedelta(hours=1),
        "sub":str(sub)
        }
    token = jwt.encode(payload,SECRET_KEY,algorithm="HS512")
    return token
    
 
def password_create(password: str):
    return password_enc.hash(password)
    
def password_verify(password: str, encpass: str):
    return password_enc.verify(password,encpass)
