from fastapi import APIRouter
from models.usuarios import Usuario
from schemas.UsuariosSCHM import UsuarioPatchShowSCHM, UsuarioPatchSCHM

router = APIRouter()



@router.post("/")
async def create(usuario: Usuario):
    return await usuario.save()

@router.get("/{id}")
async def get_id(id: int):
    return await Usuario.objects.get(id=id)

@router.get("/")
async def get_all():
    return await Usuario.objects.all()

@router.patch("/{id}",response_model=UsuarioPatchShowSCHM)
async def update_put(id: int, user: UsuarioPatchSCHM):
    user_dict = user.dict(exclude_unset=True)
    userid = await Usuario.objects.get_or_none(id=id)
    await userid.update(**user_dict)
    userid.save()
    return userid

@router.delete("/{id}")
async def delete(id:int):
    return await Usuario.objects.delete(id=id)
