from fastapi import APIRouter, Depends,Form, HTTPException, Response,status
from controllers.utils.security import get_current_user, password_verify ,jwt_create
from models.usuarios import Usuario
from schemas.UsuariosSCHM import UsuarioResponse, UsuarioResponseAll,UsuarioSCHM

router = APIRouter()

@router.post("/token",tags=["Auth"])
async def login(username: str = Form(...), password:str = Form(...)):
    user = await Usuario.objects.get_or_none(username=username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    if password_verify(password,user.hash_password):
        return {
            "access_token": jwt_create(user.id),
            "token_type": "bearer"
        }
    else:
        raise HTTPException(
            status_code=404
        )

@router.get("/me",response_model=UsuarioResponseAll,response_model_exclude_unset=True,tags=["Auth"])
async def me(user: UsuarioSCHM = Depends(get_current_user)):
    return user
    
