from typing import List, Optional
from pydantic import BaseModel, Field, validator
from controllers.utils.security import password_create


class UsuarioResponse(BaseModel):
    id:  Optional[int]
    username: str
    email: str
    cargos: List[str]
    
class UsuarioSCHM(BaseModel):
    id: int
    username: str
    email: str
    cargos: List[str]
    hash_password: str
    

    
class UsuarioPatchShowSCHM(BaseModel):
    email: str
    username: str
    
class UsuarioLogin(BaseModel):
    username: str
    email: str
    
class UsuarioCreate(BaseModel):
    email: str
    username:str
    hash_password: str = Field(alias="password")
    
    @validator('hash_password')
    def hash_pass(cls,password):
        return password_create(password)
    
class UsuarioPatchSCHM(BaseModel):
    username: Optional[str]
    email: Optional[str]
    hash_password: Optional[str] = Field(alias="password")