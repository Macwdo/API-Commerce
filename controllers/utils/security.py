from datetime import datetime, timedelta, timezone
from typing import Any, Union
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from models.usuarios import Usuario
from passlib.context import CryptContext

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='/api/auth/token'
)

password_enc = CryptContext(schemes=["sha256_crypt"],deprecated="auto")

SECRET_KEY = "djsa0iojdosa"


def jwt_create(sub: Union[Any,str]):
    payload = {
        "exp": datetime.now(tz=timezone.utc) + timedelta(hours=1),
        "sub":str(sub)
        }
    token = jwt.encode(payload,SECRET_KEY,algorithm="HS512")
    return token



def jwt_decode(token: str):
    try:
        data = jwt.decode(token,SECRET_KEY,algorithms="HS512")
        return int(data.get('sub'))
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )

async def get_current_user(token: str = Depends(oauth2_scheme)):
    id = jwt_decode(token)
    user = await Usuario.objects.get_or_none(id=int(id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
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

