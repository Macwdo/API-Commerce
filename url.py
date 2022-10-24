from fastapi import APIRouter
from controllers.usuarios_controllers import router as userroute
from controllers.usuario_auth import router as authroute
from controllers.produtos_controllers import router as produtoroute

router = APIRouter()

router.include_router(userroute, prefix="/usuarios")
router.include_router(authroute, prefix="/auth")
router.include_router(produtoroute, prefix="/produtos")

