from datetime import datetime, timedelta, timezone
from typing import Any, Union
from fastapi import Depends, HTTPException
from jose import jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from models.usuarios import Usuario


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='/api/auth/token'
)

password_enc = CryptContext(schemes=["sha256_crypt"],deprecated="auto")

SECRET_KEY = "djsa0iojdosa"


def jwt_create(sub: Union[Any,str]):
    payload = {
        "exp": datetime.now(tz=timezone.utc) + timedelta(hours=24),
        "sub":str(sub)
        }
    token = jwt.encode(payload,SECRET_KEY,algorithm="HS512")
    return token


def get_sub(token: str):
    data = jwt.decode(token,SECRET_KEY,algorithms="HS512")
    return int(data.get('sub'))

async def get_current_user(token: str = Depends(oauth2_scheme)):
    id = get_sub(token)
    user = await Usuario.objects.get_or_none(id=int(id))
    if not user:
        raise HTTPException(
            status_code=404
        )
    return user
        
def password_create(password: str):
    return password_enc.hash(password)
    
def password_verify(password: str, encpass: str):
    return password_enc.verify(password,encpass)

#####

def permission(user,permission:str):
    user = user.dict()
    cargos = user.get('cargos')
    for i in cargos:
        if permission == i:
            return True
    return False

