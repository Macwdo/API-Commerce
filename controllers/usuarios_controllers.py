from typing import List
from fastapi import APIRouter, Depends
from models.usuarios import Usuario
from schemas.UsuariosSCHM import UsuarioPatchShowSCHM, UsuarioPatchSCHM, UsuarioCreate, UsuarioLogin, UsuarioResponse
from jose import jwt
from controllers.utils.security import oauth2_scheme, verify_user


router = APIRouter()

    
@router.post("/{id}/cargos/{cargo}",response_model=UsuarioResponse,tags=["Usuario"])
async def cargos(cargo: str,id: int,token: str = Depends(oauth2_scheme)):
    user = await Usuario.objects.get_or_none(id=id)
    user.cargos += [cargo]
    await user.update()
    return user

@router.delete("/{id}/cargos/{cargo}",response_model=UsuarioResponse,tags=["Usuario"])
async def delete_cargos(cargo: str,id: int,token: str = Depends(oauth2_scheme)):
    user = await Usuario.objects.get_or_none(id=id)
    user_cargos = user.cargos
    user_cargos.remove(cargo)
    await user.update()
    return user

@router.get("/{id}",response_model=UsuarioLogin,tags=["Usuario"])
async def get_id(id: int):
    return await Usuario.objects.get(id=id)

@router.get("/",response_model=List[UsuarioResponse],tags=["Usuario"])
async def get_all():
    return await Usuario.objects.all()

@router.patch("/{id}",response_model=UsuarioPatchShowSCHM,tags=["Usuario"])
async def update_patch(id: int, user: UsuarioPatchSCHM,token: str = Depends(oauth2_scheme)):
    verify_user(id,token)
    user_dict = user.dict(exclude_unset=True)
    userid = await Usuario.objects.get_or_none(id=id)
    await userid.update(**user_dict)
    userid.save()
    return userid


@router.delete("/{id}",tags=["Usuario"])
async def delete(id:int,token: str = Depends(oauth2_scheme)):
    return await Usuario.objects.delete(id=id)
