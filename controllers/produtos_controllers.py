from controllers.utils.security import get_current_user, permission
from modelos.Produtos import Produto
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.ProdutosSCHM import ProdutoCreate

router = APIRouter()

@router.get("/",tags=["Produtos"])
async def get_all():
    return await Produto.objects.all()

@router.post("/",tags=["Produtos"], response_model=ProdutoCreate)
async def create(produto: Produto, user = Depends(get_current_user)):
    if permission(user,'vendedor'):
        return await produto.save()
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )