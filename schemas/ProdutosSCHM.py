from pydantic import BaseModel, Json


class ProdutoResponse(BaseModel):
    id: int
    nome: str
    descricao: str
    preco: float
    quantidade: int
    
class ProdutoPatch(BaseModel):
    nome: str or None = None
    descricao: str or None = None
    preco: float or None = None
    quantidade: int or None = None
    

    