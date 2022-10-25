import sys
sys.path.append("/home/danilo/Estudos/Api-Alunos/modelos")
sys.path.append("/home/danilo/Estudos/Api-Alunos")
import modelos.Usuarios
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
    vendedor: int = ormar.ForeignKey(modelos.Usuarios.Usuario,skip_reverse=True)
    preco: float = ormar.Float()