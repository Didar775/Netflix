from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_user
from app.schemes.user import UserRead
from db.models import User

router = APIRouter()

@router.get("/profile", response_model=UserRead)
def profile(user: User = Depends(get_current_user)):
    return user

