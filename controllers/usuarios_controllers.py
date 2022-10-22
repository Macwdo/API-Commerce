from typing import List
from fastapi import APIRouter, Depends, Form, HTTPException
from models.usuarios import Usuario
from schemas.UsuariosSCHM import UsuarioPatchShowSCHM, UsuarioPatchSCHM, UsuarioCreate, UsuarioLogin, UsuarioResponse
from security import password_verify ,jwt_create, oauth2_scheme, SECRET_KEY
from jose import jwt


router = APIRouter()


@router.post("/login")
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

@router.get("/gettoken")
async def getoken(token: str = Depends(oauth2_scheme)):
    
    dados = jwt.decode(token,key=SECRET_KEY,algorithms="HS512")
    return {"token": dados}


@router.post("/", response_model=UsuarioLogin)
async def create(usuario: UsuarioCreate):
    data = usuario.dict(exclude_unset=True)
    user = Usuario(**data)
    return await user.save()
    

@router.get("/{id}",response_model=UsuarioLogin)
async def get_id(id: int):
    return await Usuario.objects.get(id=id)

@router.get("/",response_model=List[UsuarioResponse])
async def get_all():
    return await Usuario.objects.all()

@router.patch("/{id}",response_model=UsuarioPatchShowSCHM)
async def update_patch(id: int, user: UsuarioPatchSCHM):
    user_dict = user.dict(exclude_unset=True)
    userid = await Usuario.objects.get_or_none(id=id)
    await userid.update(**user_dict)
    userid.save()
    return userid

@router.delete("/{id}",)
async def delete(id:int,token: str = Depends(oauth2_scheme)):
    return await Usuario.objects.delete(id=id)
