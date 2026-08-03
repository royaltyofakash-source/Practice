from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.schemas.requestSchemas import LoginRequest
from app.auth.schemas.responseSchemas import TokenResponse
from app.auth.services import authServices as auth_service

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    return auth_service.login_user(db, data.email, data.password)
