from fastapi import APIRouter,Depends,Response,HTTPException,status
from controllers.utils.security import permission, get_current_user
from models.usuarios import Usuario
from schemas.UsuariosSCHM import UsuarioResponse,UsuarioSCHM


router = APIRouter()


@router.get("/{id}/cargos/{cargo}",response_model=UsuarioResponse,tags=["Usuario"])
async def cargos(cargo: str,id: int,user: UsuarioSCHM = Depends(get_current_user)):
    if permission(user,'admin') or 1==1:
        usuario = await Usuario.objects.get_or_none(id=id)
        usuario.cargos += [cargo]
        await usuario.update()
        return usuario
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )

@router.delete("/{id}/cargos/{cargo}",response_model=UsuarioResponse,tags=["Usuario"])
async def delete_cargos(cargo: str,id: int,user: UsuarioSCHM = Depends(get_current_user), response: Response = Response()):
    dados = user.dict()
    id_user = int(dados.get('id'))
    if permission(user,'admin') or 1==1:
        if id_user != id:
            usuario = await Usuario.objects.get_or_none(id=id)
            user_cargos = usuario.cargos
            if len(user_cargos) == 0:
                response.status_code = status.HTTP_404_NOT_FOUND
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Cargo não encontrado")
            user_cargos.remove(cargo)
            await usuario.update()
            return usuario
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )