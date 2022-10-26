from fastapi import APIRouter
from controllers.usuarios_controllers import router as userroute
from controllers.usuario_auth import router as authroute
from controllers.produtos_controllers import router as produtoroute
from controllers.cargos_controllers import router as cargoroute
from controllers.pedidos_controllers import router as pedidoroute

router = APIRouter()

router.include_router(authroute, prefix="/auth")
router.include_router(userroute, prefix="/usuarios")
router.include_router(produtoroute, prefix="/usuarios")
router.include_router(cargoroute, prefix="/usuarios")
router.include_router(pedidoroute, prefix="/usuarios")

