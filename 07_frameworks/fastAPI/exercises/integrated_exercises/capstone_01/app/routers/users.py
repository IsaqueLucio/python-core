from fastapi import APIRouter, Depends
from app.schemas import UserOut
import app.models
from app.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserOut)
def get_me(current_user: app.models.User = Depends(get_current_user)):
    return current_user


