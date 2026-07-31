from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.shared.database.session import get_db
from app.auth.schemas.request import RegisterRequest
from app.auth.schemas.response import UserResponse
from app.auth.services import auth_service

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    return auth_service.register_user(db, data.fullname, data.email, data.password)
