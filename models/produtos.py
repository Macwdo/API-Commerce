from models.usuarios import Usuario
import ormar
from configs.database import metadata, database

class Produto(ormar.Model):
    class Meta:
        database = database
        metadata =  metadata
        tablename = "Produtos"
        
    id: int = ormar.Integer(primary_key=True)
    nome: str = ormar.String(max_length=50)
    descricao: str = ormar.String(max_length=200)
    vendedor: int = ormar.ForeignKey(Usuario, skip_reverse=True)
    quantidade: int = ormar.Integer()
    preco: float = ormar.Float()