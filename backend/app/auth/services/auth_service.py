from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.auth.repositories import auth_repository
from app.shared.security import create_access_token

def register_user(db: Session, fullname: str, email: str, password: str):
    existing_user = auth_repository.get_user_by_email(db, email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = auth_repository.create_user(db, fullname, email, password)
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer", "user": user}

def login_user(db: Session, email: str, password: str):
    user = auth_repository.get_user_by_email(db, email)
    if not user or user.password != password:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer", "user": user}
