import ormar
from pydantic import validator
from configs.database import database, metadata


cargos_validos = ['admin','vendedor','comprador']


class Usuario(ormar.Model):
    class Meta:
        database = database
        metadata =  metadata
        tablename = "Usuario"
    id : int = ormar.Integer(primary_key=True)
    username: str = ormar.String(max_length=30,unique=True)
    email: str = ormar.String(max_length=120,unique=True)
    hash_password: str = ormar.String(max_length=256)
    cargos: str = ormar.JSON(default=[])

    @validator("cargos")
    def cargos_duplicate_validator(cls,v):
        return list(set(v))
    
    @validator("cargos")
    def cargos_valido(cls,v):
        if not isinstance(v,list):
            raise ValueError(f"Os Cargo do usuario deve ser uma lista")
        for cargo in v:
            if not isinstance(cargo, str) or cargo not in cargos_validos:
                raise ValueError(f"A Cargo {cargo} não existe")
        return v
    


        
    
        