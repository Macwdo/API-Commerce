from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Response, status
from models.produtos import Produto
from models.usuarios import Usuario
from schemas.ProdutosSCHM import ProdutoResponse
from schemas.UsuariosSCHM import UsuarioPatchShowSCHM, UsuarioPatchSCHM, UsuarioLogin, UsuarioResponse, UsuarioResponseAll, UsuarioSCHM,UsuarioCreate
from controllers.utils.security import oauth2_scheme, get_current_user, permission


router = APIRouter()

    
@router.post("/", response_model=UsuarioLogin,tags=["Usuario"])
async def create(usuario: UsuarioCreate,response : Response = Response()):
    response.status_code = status.HTTP_201_CREATED
    data = usuario.dict(exclude_unset=True)
    user = Usuario(**data)
    return  await user.save()

@router.get("/{id}",response_model=UsuarioResponseAll,response_model_exclude_unset=True,tags=["Usuario"])
async def get_id(id: int):
    user = await Usuario.objects.get(id=id)
    response = []
    id_vend = {"vendedor":user.id}
    produtos = await Produto.objects.all(**id_vend)
    response = {
        "id": int(user.id),
        "username": user.username,
        "email": user.email,
        "cargos": user.cargos,
        "vendas": produtos,
    }
    return response


@router.get("/",response_model=List[UsuarioResponseAll],response_model_exclude_unset=True,tags=["Usuario"])
async def get_all(page_num: int = 1,page_size: int = 10):
    start = (page_num - 1) * page_size
    end = start + page_size
    users = await Usuario.objects.all()
    response = []
    for user in users:
        id_vend = {"vendedor":user.id}
        produtos = await Produto.objects.all(**id_vend)
        data = {
            "id": int(user.id),
            "username": user.username,
            "email": user.email,
            "cargos": user.cargos,
            "vendas": produtos,
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
        status_code=401,
        detail="Not authenticated"
     )

