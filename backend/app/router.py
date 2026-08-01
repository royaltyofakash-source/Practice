from fastapi import APIRouter
from app.auth.routes.router import router as auth_router
from app.auth.routes import documents

router = APIRouter()

router.include_router(auth_router)
router.include_router(documents.router)
