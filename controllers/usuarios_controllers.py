from typing import List
from fastapi import APIRouter, Depends, HTTPException
from models.usuarios import Usuario
from schemas.UsuariosSCHM import UsuarioPatchShowSCHM, UsuarioPatchSCHM, UsuarioLogin, UsuarioResponse
from controllers.utils.security import oauth2_scheme, get_current_user, admin_permission


router = APIRouter()

    
@router.post("/{id}/cargos/{cargo}",response_model=UsuarioResponse,tags=["Usuario"])
async def cargos(cargo: str,id: int,user: UsuarioResponse = Depends(get_current_user)):
    if admin_permission:
        usuario = await Usuario.objects.get_or_none(id=id)
        usuario.cargos += [cargo]
        await usuario.update()
        return usuario
    else:
        raise HTTPException(
        status=401,
        details={"detail":"Not authenticated"}
    )
        

@router.delete("/{id}/cargos/{cargo}",response_model=UsuarioResponse,tags=["Usuario"])
async def delete_cargos(cargo: str,id: int,user: str = Depends(get_current_user)):
    usuario = await Usuario.objects.get_or_none(id=id)
    user_cargos = usuario.cargos
    user_cargos.remove(cargo)
    await usuario.update()
    return usuario

@router.get("/{id}",response_model=UsuarioLogin,tags=["Usuario"])
async def get_id(id: int):
    return await Usuario.objects.get(id=id)

@router.get("/",response_model=List[UsuarioResponse],tags=["Usuario"])
async def get_all():
    return await Usuario.objects.all()

@router.patch("/{id}",response_model=UsuarioPatchShowSCHM,tags=["Usuario"])
async def update_patch(id: int, user_data: UsuarioPatchSCHM,user: str = Depends(get_current_user)):
    user_dict = user_data.dict(exclude_unset=True)
    userid = await Usuario.objects.get_or_none(id=id)
    await userid.update(**user_dict)
    userid.save()
    return userid


@router.delete("/{id}",tags=["Usuario"])
async def delete(id:int,user: str = Depends(get_current_user)):
    return await Usuario.objects.delete(id=id)
