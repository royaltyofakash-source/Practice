from fastapi import APIRouter
from app.auth.routes.Auth_router_Routes import router as auth_router
from app.auth.routes import Auth_documents_Routes as documents

router = APIRouter()

router.include_router(auth_router)
router.include_router(documents.router)
