from fastapi import APIRouter
from app.auth.routes import register, login

router = APIRouter(prefix="/auth")

router.include_router(register.router)
router.include_router(login.router)
