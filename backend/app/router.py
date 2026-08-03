from fastapi import APIRouter
from app.auth.routes.routerRoutes import router as auth_router
from app.rag.routes import documentsRoutes as documents

router = APIRouter()

router.include_router(auth_router)
router.include_router(documents.router)
