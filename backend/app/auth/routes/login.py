from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.shared.database.session import get_db
from app.auth.schemas.request import LoginRequest
from app.auth.schemas.response import UserResponse
from app.auth.services import auth_service

router = APIRouter()

@router.post("/login", response_model=UserResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    return auth_service.login_user(db, data.email, data.password)
