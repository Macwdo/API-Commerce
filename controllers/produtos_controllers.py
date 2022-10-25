from typing import List
from controllers.utils.security import get_current_user, permission
from models.produtos import Produto
from fastapi import APIRouter, Depends, HTTPException, status, Response
from schemas.ProdutosSCHM import ProdutoPatch, ProdutoResponse
from schemas.UsuariosSCHM import UsuarioSCHM

router = APIRouter()

#Gets

@router.get("/produtos/",tags=["Produtos"])
async def get_all():
    return await Produto.objects.all()

@router.get("/produtos/{id_pd}",tags=["Produtos"])
async def get_id_prod(id_pd: int):
    produto = await Produto.objects.get_or_none(id=id_pd)
    if produto is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND
        )
    return produto

@router.get("/{id_us}/produtos",tags=["Produtos"])
async def get_all_user_prod(id_us: int):
    vend = {"vendedor":id_us}
    return await Produto.objects.all(**vend)


#Posts

@router.post("/produtos",tags=["Produtos"], response_model=ProdutoResponse)
async def create(produto: Produto, user = Depends(get_current_user)):
    if permission(user,'vendedor'):
        return await produto.save()
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTzHORIZED
        )
    
#Patch

@router.patch("/produtos/{id_pd}",response_model=ProdutoResponse,tags=["Produtos"])
async def update_patch(id_pd: int, prod_data: ProdutoPatch,user: UsuarioSCHM = Depends(get_current_user),response: Response = Response()):
    produto_id = await Produto.objects.get_or_none(id=id_pd)
    id_vendedor = dict(produto_id.vendedor)
    if permission(user,'admin') or user.id == int(id_vendedor.get("id")):
        produto_dict = prod_data.dict(exclude_unset=True)
        await produto_id.update(**produto_dict)
        produto_id.save()
        response.status_code = status.HTTP_206_PARTIAL_CONTENT
        return produto_id
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )
        
#delete

@router.delete("/produtos/{id_pd}",tags=["Produto"])
async def delete(id_pd: int,user: UsuarioSCHM = Depends(get_current_user),response: Response = Response()):
    produto_id = await Produto.objects.get_or_none(id=id_pd)
    if not produto_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    id_vendedor = dict(produto_id.vendedor)
    if permission(user, 'admin') or int(id_vendedor.get("id")) == user.id:
        response.status_code = status.HTTP_204_NO_CONTENT
        return await Produto.objects.delete(id=id_pd)
    else:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED
     )
