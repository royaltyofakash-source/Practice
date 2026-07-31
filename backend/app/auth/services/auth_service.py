from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.auth.repositories import auth_repository

def register_user(db: Session, fullname: str, email: str, password: str):
    existing_user = auth_repository.get_user_by_email(db, email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return auth_repository.create_user(db, fullname, email, password)

def login_user(db: Session, email: str, password: str):
    user = auth_repository.get_user_by_email(db, email)
    if not user or user.password != password:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    return user
