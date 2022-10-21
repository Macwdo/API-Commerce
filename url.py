from fastapi import APIRouter
from controllers.usuarios_controllers import router as userroute


router = APIRouter()
router.include_router(userroute, prefix="/usuarios")