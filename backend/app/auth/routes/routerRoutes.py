from fastapi import APIRouter
from app.auth.routes import registerRoutes as register, loginRoutes as login

router = APIRouter(prefix="/auth")

router.include_router(register.router)
router.include_router(login.router)
