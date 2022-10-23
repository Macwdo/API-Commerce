from fastapi import APIRouter, Depends,Form, HTTPException
from controllers.utils.security import password_verify ,jwt_create, SECRET_KEY,jwt_decode,oauth2_scheme
from models.usuarios import Usuario
from schemas.UsuariosSCHM import UsuarioLogin, UsuarioCreate, UsuarioResponse

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

@router.get("/me",response_model=UsuarioResponse)
async def me(token: str = Depends(oauth2_scheme)):
    id = jwt_decode(token)
    user = await Usuario.objects.get_or_none(id=int(id))
    return user
    

@router.post("/", response_model=UsuarioLogin,tags=["Usuario"])
async def create(usuario: UsuarioCreate):
    data = usuario.dict(exclude_unset=True)
    user = Usuario(**data)
    return await user.save()