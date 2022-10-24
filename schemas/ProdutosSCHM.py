from pydantic import BaseModel, Json

from models.usuarios import Usuario



class ProdutoCreate(BaseModel):
    id: int
    nome: str
    descricao: str
    preco: float