import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.schemes.auth import TokenResponse, Token, LoginResponse
from app.schemes.user import UserCreate, UserRead
from app.services.auth import Authentication
from app.services.exceptions import InvalidCredentials, UserAlreadyExists
from app.services.userservice import UserService

router = APIRouter()

@router.post("/register", response_model=UserRead)
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return UserService(db).register(user)
    except UserAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=str(e))


@router.post("/login", response_model=LoginResponse)
def login(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return UserService(db).login(email=str(user.email),
                             password=user.password)

    except InvalidCredentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid credentials")



@router.post("/refresh", response_model=TokenResponse)
def refresh_token(token: Token, db = Depends(get_db)):
    auth = Authentication(db=db)

    try:
        user_id = auth.verify_refresh_token(token.token)
        return auth.create_access_token(user_id=user_id)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401,
                            detail="Refresh token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401,
                            detail="Invalid refresh token")