from fastapi import APIRouter, Depends, HTTPException, Response,status
from controllers.utils.security import get_current_user, permission
from models.pedidos import Pedido
from models.produtos import Produto
from models.usuarios import Usuario
from schemas.PedidosSCHM import PedidosClientPatchSCHM, PedidosClientSCHM
from schemas.UsuariosSCHM import UsuarioSCHM
from datetime import datetime


router = APIRouter()


@router.get("/pedidos/",tags=["Pedidos"],)
async def get_all(user: UsuarioSCHM = Depends(get_current_user)):
    if permission(user,"admin"):
        pedido = await Pedido.objects.all()
    else:
        pedido_user_id = await Usuario.objects.get_or_none(id=user.id)
        pedido = await Pedido.objects.all(comprador=pedido_user_id.id)
    return pedido

@router.get("/pedidos/entregue",tags=["Pedidos"],)
async def get_all_entregues(user: UsuarioSCHM = Depends(get_current_user)):
    if not permission(user,"admin"):
        pedido = await Pedido.objects.all(id=user.id,entregue=True)
    else:
        pedido = await Pedido.objects.all(entregue=True)
    return pedido


@router.get("/pedidos/{id}",tags=["Pedidos"])
async def get_id(id: int, user: UsuarioSCHM = Depends(get_current_user)):
    pedido = await Pedido.objects.get_or_none(id=id)
    if not pedido:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND
        )
    pedido_data = pedido.dict()
    pedido_comprador_id , pedido_produto_id = dict(pedido_data.get("comprador")), dict(pedido_data.get("produto"))
    vendedor_produto_id = await Produto.objects.get(**pedido_produto_id)
    id_vendedor = vendedor_produto_id.vendedor
    if pedido_comprador_id.get("id") == user.id or id_vendedor == user.id or permission(user,"admin"):
        return pedido
    else:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED
        )

@router.post("/pedidos/",tags=["Pedidos"])
async def create(pedido: PedidosClientSCHM,user: UsuarioSCHM = Depends(get_current_user)):
    if not permission(user,"comprador") or permission(user,"admin"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )
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
    pedido_produto_dict = dict(pedido.produto)
    produto_dict, produto = dict(await Produto.objects.get_or_none(id=pedido_produto_dict.get("id"))), await Produto.objects.get_or_none(id=pedido_produto_dict.get("id"))
    produto_id = dict(produto_dict.get("vendedor"))
    if permission(user,"vendedor") and user.id == produto_id.get('id') or permission(user,"admin"):
        if pedido.entregue:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Pedido já Entregue"
            )
        pedido.entregue = True
        produto.quantidade -= pedido.quantidade
        if produto.quantidade < 0:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Capacidade Indisponivel no Estoque"
            )
        await produto.update()
        await pedido.update()
        return pedido
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )

@router.delete("/pedidos/{id}",tags=["Pedidos"])
async def apagar_pedido(id: int, user: UsuarioSCHM = Depends(get_current_user), response: Response = Response()):
    pedido = await Pedido.objects.get_or_none(id=id)
    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    produto_dict = dict(pedido.comprador)
    if permission(user,"comprador") and user.id == produto_dict.get("id") or permission(user,"admin"):
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
    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    if pedido.entregue:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="O Produto ja foi entregue"
        )
    comprador_dict = dict(pedido.comprador)
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
        
    
