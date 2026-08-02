from fastapi import APIRouter
from app.auth.routes import Auth_register_Routes as register, Auth_login_Routes as login

router = APIRouter(prefix="/auth")

router.include_router(register.router)
router.include_router(login.router)
