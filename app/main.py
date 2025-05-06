
from fastapi import FastAPI
from . import models
from .database import engine
from .routes import auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)
