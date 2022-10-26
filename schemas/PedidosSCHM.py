from datetime import datetime
from itertools import count
from pydantic import BaseModel, validator

from models.produtos import Produto


class PedidosClientSCHM(BaseModel):
    produto: int
    quantidade: int
    endereco: str
    observacao: str
    
class PedidosClientPatchSCHM(BaseModel):
    endereco: str or None = None
    observacao: str or None = None
        
        
    
class PedidosResponseSCHM(BaseModel):
    id: int
    comprador: int
    produto: int
    quantidade: int
    endereco: str
    observacao: str
    preco: float
    data: datetime
    entregue: bool
