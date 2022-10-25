from pydantic import BaseModel, Json

from modelos.Usuarios import Usuario



class ProdutoCreate(BaseModel):
    id: int
    nome: str
    descricao: str
    preco: float
    