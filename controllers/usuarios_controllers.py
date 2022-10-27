from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Response, status
from models.pedidos import Pedido
from models.produtos import Produto
from models.usuarios import Usuario
from schemas.ProdutosSCHM import ProdutoResponse
from schemas.UsuariosSCHM import UsuarioPatchShowSCHM, UsuarioPatchSCHM, UsuarioLogin, UsuarioResponse, UsuarioResponseAll, UsuarioSCHM,UsuarioCreate
from controllers.utils.security import oauth2_scheme, get_current_user, permission


router = APIRouter()

    
@router.post("/comprador", response_model=UsuarioLogin,tags=["Usuario"])
async def criar_comprador(usuario: UsuarioCreate,response : Response = Response()):
    response.status_code = status.HTTP_201_CREATED
    data = usuario.dict(exclude_unset=True)
    user = Usuario(**data,cargos="comprador")
    print(user)
    return await user.save()

@router.post("/vendedor", response_model=UsuarioLogin,tags=["Usuario"])
async def criar_vendedor(usuario: UsuarioCreate,response : Response = Response()):
    response.status_code = status.HTTP_201_CREATED
    data = usuario.dict(exclude_unset=True)
    user = Usuario(**data)
    return await user.save()

@router.get("/",response_model=List[UsuarioResponse],tags=["Usuario"])
async def get_users():
    return await Usuario.objects.all()

@router.get("/{id}",response_model=UsuarioResponse,tags=["Usuario"])
async def get_users_id(id: int):
    return await Usuario.objects.get(id=id)

@router.get("/admin/{id}",response_model=UsuarioResponseAll,response_model_exclude_unset=True,tags=["Usuario"])
async def get_id(id: int):
    user = await Usuario.objects.get(id=id)
    response = []
    id_vend = {"vendedor":user.id}
    produtos = await Produto.objects.all(**id_vend)
    id_comp = {"comprador":user.id}
    pedidos = await Pedido.objects.all(**id_comp)
    response = {
        "id": int(user.id),
        "username": user.username,
        "email": user.email,
        "cargos": user.cargos,
        "vendas": produtos,
        "pedidos": pedidos
    }
    return response

@router.get("/admin/",response_model=List[UsuarioResponseAll],response_model_exclude_unset=True,tags=["Usuario"])
async def admin_listviewpage(page: int = 1,page_size: int = 10, user: UsuarioSCHM = Depends(get_current_user)):
    if not permission(user,"admin"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    start = (page - 1) * page_size
    end = start + page_size
    users = await Usuario.objects.all()
    response = []
    for usuario in users:
        id_vend = {"vendedor":usuario.id}
        produtos = await Produto.objects.all(**id_vend)
        id_comp = {"comprador":usuario.id}
        pedidos = await Pedido.objects.all(**id_comp)
        data = {
            "id": int(usuario.id),
            "username": usuario.username,
            "email": usuario.email,
            "cargos": usuario.cargos,
            "vendas": produtos,
            "pedidos": pedidos
        }
        response.append(data)
    return response[start:end]


@router.patch("/{id}",response_model=UsuarioPatchShowSCHM,tags=["Usuario"])
async def update_patch(id: int, user_data: UsuarioPatchSCHM,user: UsuarioSCHM = Depends(get_current_user),response: Response = Response()):
    if permission(user,'admin') or id == user.id:
        user_dict = user_data.dict(exclude_unset=True)
        userid = await Usuario.objects.get_or_none(id=id)
        await userid.update(**user_dict)
        userid.save()
        response.status_code = status.HTTP_206_PARTIAL_CONTENT
        return userid

@router.delete("/{id}",tags=["Usuario"])
async def delete(id:int,user: UsuarioSCHM = Depends(get_current_user),response: Response = Response()):
    if permission(user,'admin'):
        if id != user.id:
            userobj = await Usuario.objects.get_or_none(id=id)
            if not userobj:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Not Found"
                )
            response.status_code = status.HTTP_204_NO_CONTENT
            return await Usuario.objects.delete(id=id)
        else:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Not Acceptable"
            )
    else:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED
     )

