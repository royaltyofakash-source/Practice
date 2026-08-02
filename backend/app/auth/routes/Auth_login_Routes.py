from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.auth.Auth_database import get_db
from app.auth.schemas.Auth_request_Schemas import LoginRequest
from app.auth.schemas.Auth_response_Schemas import TokenResponse
from app.auth.services import Auth_auth_Services as auth_service

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    return auth_service.login_user(db, data.email, data.password)
