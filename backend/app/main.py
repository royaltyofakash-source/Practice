from fastapi import FastAPI
from app.shared.database.base import Base, engine
from app.router import router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)
