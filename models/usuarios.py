import ormar
from configs.database import database, metadata



class Usuario(ormar.Model):
    class Meta:
        database = database
        metadata =  metadata
        tablename = "Usuario"
        
    id : int = ormar.Integer(primary_key=True)
    username: str = ormar.String(max_length=30,unique=True)
    email: str = ormar.String(max_length=120,unique=True)
    hash_password: str = ormar.String(max_length=256)
    
         
        
    
        