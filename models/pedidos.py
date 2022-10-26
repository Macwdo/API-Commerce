from datetime import datetime
from email.policy import default
import ormar
from configs.database import database, metadata
from models.usuarios import Usuario
from models.produtos import Produto


class Pedido(ormar.Model):
    class Meta:
        database = database
        metadata = metadata
        tablename = "Pedidos"
        
    id: int =  ormar.Integer(primary_key=True)
    quantidade: int = ormar.Integer()
    preco: float = ormar.Float()
    endereco: str = ormar.String(max_length=150)
    observacao: str = ormar.String(max_length=350)
    data: datetime = ormar.DateTime()
    comprador: int = ormar.ForeignKey(Usuario, skip_reverse=True)
    produto: int = ormar.ForeignKey(Produto, skip_reverse=True)
    entregue: bool = ormar.Boolean(default=False)
    