from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.auth.Auth_database import get_db
from app.auth.schemas.Auth_request_Schemas import RegisterRequest
from app.auth.schemas.Auth_response_Schemas import TokenResponse
from app.auth.services import Auth_auth_Services as auth_service

router = APIRouter()

@router.post("/register", response_model=TokenResponse)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    return auth_service.register_user(db, data.fullname, data.email, data.password)
