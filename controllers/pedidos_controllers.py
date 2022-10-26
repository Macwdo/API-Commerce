from fastapi import APIRouter, Depends, HTTPException, Response,status
from controllers.utils.security import get_current_user, permission
from models.pedidos import Pedido
from models.produtos import Produto
from schemas.PedidosSCHM import PedidosClientPatchSCHM, PedidosClientSCHM, PedidosResponseSCHM
from schemas.UsuariosSCHM import UsuarioSCHM
from datetime import datetime


router = APIRouter()


@router.get("/pedidos/",tags=["Pedidos"])
async def get_all():
    return await Pedido.objects.all()

@router.get("/pedidos/{id}",tags=["Pedidos"])
async def get_id(id: int):
    return await Pedido.objects.get(id=id)

@router.post("/pedidos/",tags=["Pedidos"])
async def create(pedido: PedidosClientSCHM,user: UsuarioSCHM = Depends(get_current_user)):
    if permission(user,"comprador"):
        data = pedido.dict()
        time_now = datetime.now()
        produto_id = data.get("produto")
        produto = await Produto.objects.get_or_none(id=produto_id)
        if not produto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND
            )
        quantidade = data.get("quantidade")
        if quantidade > produto.quantidade:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Pedido maior que o estoque. Estoque: {produto.quantidade}"
            )
        data["comprador"] = {"id":user.id}
        data["produto"] = {"id":produto.id}
        data["preco"] = produto.preco * quantidade
        data["data"] = time_now
        pedido_save = Pedido(**data)
        await pedido_save.save()
        return pedido_save.dict(exclude_unset=True)
    
@router.get("/pedidos/atualizar/{id}",tags=["Pedidos"])
async def finalizar_pedido(id: int,user: UsuarioSCHM = Depends(get_current_user)):
    pedido = await Pedido.objects.get_or_none(id=id)
    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    produto_dict = dict(pedido.produto)
    if permission(user,"vendedor") or permission(user,"admin") and user.id == produto_dict.get("id"):
        pedido.entregue = True
        await pedido.update()
    return pedido

@router.delete("/pedidos/{id}",tags=["Pedidos"])
async def apagar_pedido(id: int, user: UsuarioSCHM = Depends(get_current_user), response: Response = Response()):
    pedido = await Pedido.objects.get_or_none(id=id)
    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    produto_dict = dict(pedido.produto)
    if permission(user,"vendedor") and user.id == produto_dict.get("id") or permission(user,"admin"):
        if permission(user,"admin") or pedido.entregue:
            response.status_code = status.HTTP_204_NO_CONTENT
            return await pedido.delete()
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )
        
@router.patch("/pedidos/{id}",tags=["Pedidos"])
async def atualizar_pedido(id: int, dados: PedidosClientPatchSCHM,user: UsuarioSCHM = Depends(get_current_user),response: Response = Response()):
    dados = dados.dict(exclude_unset=True)
    pedido = await Pedido.objects.get_or_none(id=id)
    comprador_dict = dict(pedido.comprador)
    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    if permission(user,"comprador") and user.id == comprador_dict.get("id") or permission(user,"admin"):
        if permission(user,"admin") or not pedido.entregue:
            await pedido.update(**dados)
            return pedido
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )
        
    
