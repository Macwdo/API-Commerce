import ormar
from configs.database import database, metadata
from pydantic import validator
from security import password_create


class Usuario(ormar.Model):
    class Meta:
        database = database
        metadata =  metadata
        tablename = "Usuario"
        
    id : int = ormar.Integer(primary_key=True,)
    username: str = ormar.String(max_length=30,unique=True)
    email: str = ormar.String(max_length=120,unique=True)
    hash_password: str = ormar.String(max_length=256)
    
    @validator('hash_password')
    def hash_pass(password: hash_password) -> str:
        return password_create(password)
         
        
    
        