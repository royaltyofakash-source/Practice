from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    password = Column(String)

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, fullname: str, email: str, password: str):
    new_user = User(fullname=fullname, email=email, password=password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
