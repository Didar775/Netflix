from sqlalchemy.orm import Session

import db
from app.schemes.auth import Login, LoginResponse
from app.schemes.user import UserCreate, UserRead
from app.services.auth import Authentication
from app.services.exceptions import InvalidCredentials, UserAlreadyExists
from db.models import User


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.auth = Authentication(self.db)

    def register(self, user_data: UserCreate):
        user = self.db.query(User).filter(User.email == user_data.email).first()
        if user:
            raise UserAlreadyExists(f"User {user_data.email} already exists")

        new_user = User(
            email=str(user_data.email),
            password=self.auth.hash_password(user_data.password)  # Hash password!
        )

        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)

        return new_user


    def login(self, email: str, password: str):
        user = self.db.query(User).filter(User.email == email).first()

        if not user:
            raise InvalidCredentials()

        if not self.auth.verify_password(plain_password=password,
                                         hashed_password=user.password): # type: ignore
            raise InvalidCredentials()

        access_token = self.auth.create_access_token(user_id=int(user.id))  # type: ignore
        refresh_token_str = self.auth.set_refresh_token(user=user) # type: ignore

        return LoginResponse(access_token=access_token.access_token,
                             refresh_token=refresh_token_str)

