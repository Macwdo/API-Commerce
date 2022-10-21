from datetime import datetime, timedelta, timezone
from typing import Any, Union
from passlib.context import CryptContext
from configs.database import SECRET_KEY
from jose import jwt

password_enc = CryptContext(schemes=["sha256_crypt"])

def jwt_create(sub: Union[Any,str]):
    payload = {
        "exp": datetime.now(tz=timezone.utc) + timedelta(hours=1),
        "sub":str(sub)
        }
    token = jwt.encode(payload,SECRET_KEY,algorithm="HS512")
    return token
    
 
def password_create(password: str):
    return password_enc.hash(password)
    
def password_verify(password: str):
    return password_enc.verify(password,password_create(password))
