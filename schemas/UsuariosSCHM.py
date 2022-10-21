from typing import Optional
from pydantic import BaseModel, Field

class UsuarioPatchShowSCHM(BaseModel):
    email: str
    username: str
    
class UsuarioPatchSCHM(BaseModel):
    username: Optional[str]
    email: Optional[str]
    hash_password: Optional[str] = Field(alias="password")