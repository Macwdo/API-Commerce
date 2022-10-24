from fastapi import APIRouter, Depends,Form, HTTPException, Response,status
from controllers.utils.security import get_current_user, password_verify ,jwt_create
from models.usuarios import Usuario
from schemas.UsuariosSCHM import UsuarioResponse,UsuarioSCHM

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

@router.get("/me",response_model=UsuarioResponse,tags=["Usuario"])
async def me(user: UsuarioSCHM = Depends(get_current_user)):
    return user
    
