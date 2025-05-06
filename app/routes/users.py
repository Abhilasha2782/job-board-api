from fastapi import APIRouter, Depends
from app.auth import get_current_user
from app import schemas, models

router = APIRouter()

@router.get("/users/me", response_model=schemas.UserResponse)
def read_current_user(current_user: models.User = Depends(get_current_user)):
    return current_user
