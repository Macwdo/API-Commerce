from typing import List
from fastapi import APIRouter, Depends, Form, HTTPException
from models.usuarios import Usuario
from schemas.UsuariosSCHM import UsuarioPatchShowSCHM, UsuarioPatchSCHM, UsuarioCreate, UsuarioLogin, UsuarioResponse
from security import jwt_get_sub, password_verify ,jwt_create, oauth2_scheme, SECRET_KEY
from jose import jwt


router = APIRouter()


@router.post("/login",tags=["Usuario"])
async def login(username: str = Form(...), password:str = Form(...)):
    user = await Usuario.objects.get_or_none(username=username)
    if password_verify(password,user.hash_password):
        return {
            "access_token": jwt_create(user.id),
            "token_type": "bearer"
        }
    else:
        raise HTTPException(
            status_code=404
        )

@router.get("/gettoken",tags=["Usuario"])
async def getoken(token: str = Depends(oauth2_scheme)):
    dados = jwt_get_sub(token)
    return {}


@router.post("/", response_model=UsuarioLogin,tags=["Usuario"])
async def create(usuario: UsuarioCreate):
    data = usuario.dict(exclude_unset=True)
    user = Usuario(**data)
    return await user.save()
    
@router.post("{id}/cargos/{cargo}",response_model=UsuarioResponse)
async def cargos(cargo: str,id: int):
    user = await Usuario.objects.get_or_none(id=id)
    user.cargos += [cargo]
    return user.save()

@router.get("/{id}",response_model=UsuarioLogin,tags=["Usuario"])
async def get_id(id: int):
    return await Usuario.objects.get(id=id)

@router.get("/",response_model=List[UsuarioResponse],tags=["Usuario"])
async def get_all():
    return await Usuario.objects.all()

@router.patch("/{id}",response_model=UsuarioPatchShowSCHM,tags=["Usuario"])
async def update_patch(id: int, user: UsuarioPatchSCHM,token: str = Depends(oauth2_scheme)):
    user_dict = user.dict(exclude_unset=True)
    userid = await Usuario.objects.get_or_none(id=id)
    await userid.update(**user_dict)
    userid.save()
    return userid

@router.delete("/{id}",tags=["Usuario"])
async def delete(id:int,token: str = Depends(oauth2_scheme)):
    return await Usuario.objects.delete(id=id)
