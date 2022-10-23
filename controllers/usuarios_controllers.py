from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Response, status
from models.usuarios import Usuario
from schemas.UsuariosSCHM import UsuarioPatchShowSCHM, UsuarioPatchSCHM, UsuarioLogin, UsuarioResponse, UsuarioSCHM
from controllers.utils.security import oauth2_scheme, get_current_user, permission


router = APIRouter()

    
@router.post("/{id}/cargos/{cargo}",response_model=UsuarioResponse,tags=["Usuario"])
async def cargos(cargo: str,id: int,user: UsuarioSCHM = Depends(get_current_user)):
    if permission(user,'admin'):
        usuario = await Usuario.objects.get_or_none(id=id)
        usuario.cargos += [cargo]
        await usuario.update()
        return usuario
    else:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

@router.delete("/{id}/cargos/{cargo}",response_model=Optional[UsuarioResponse],tags=["Usuario"])
async def delete_cargos(cargo: str,id: int,user: UsuarioSCHM = Depends(get_current_user), response: Response = Response()):
    dados = user.dict()
    id_user = int(dados.get('id'))
    if permission(user,'admin'):
        if id_user != id:
            usuario = await Usuario.objects.get_or_none(id=id)
            user_cargos = usuario.cargos
            if len(user_cargos) == 0:
                response.status_code = 404
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Cargo não encontrado")
            user_cargos.remove(cargo)
            await usuario.update()
            return usuario
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


@router.get("/{id}",response_model=UsuarioLogin,tags=["Usuario"])
async def get_id(id: int):
    return await Usuario.objects.get(id=id)

@router.get("/",response_model=List[UsuarioResponse],tags=["Usuario"])
async def get_all():
    return await Usuario.objects.all()

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

