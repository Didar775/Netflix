import hashlib
from datetime import datetime, timedelta
import jwt
from sqlalchemy.orm import Session

from app.schemes.auth import TokenResponse
from db.models import RefreshToken
from db.models import User


class Authentication:
    SECRET_KEY = "REFRESH_SECRET_KEY"
    ACCESS_SECRET = "ACCESS_SECRET_KEY"
    ALGORITHM = "HS256"
    HASH_ALGORITHM = ['argon2', 'bcrypt']

    def __init__(self, db: Session):
        self.db = db

    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=HASH_ALGORITHM, deprecated="auto")

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def set_refresh_token(self, user: User) -> str:
        expire = datetime.utcnow() + timedelta(days=7)
        payload = {"sub": str(user.id), "exp": expire}
        token = jwt.encode(payload, self.SECRET_KEY, self.ALGORITHM)

        refresh_token = RefreshToken(
            token=token,
            expires_at=expire,
            user_id=user.id
        )
        self.db.add(refresh_token)
        self.db.commit()

        return token

    def verify_refresh_token(self, token: str) -> int:
        refresh_token = self.db.query(RefreshToken).filter_by(token=token).first()
        if not refresh_token:
            raise jwt.InvalidTokenError()

        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            user_id = int(payload.get("sub"))
        except jwt.ExpiredSignatureError:
            raise
        except jwt.InvalidTokenError:
            raise

        return user_id

    def create_access_token(self, user_id: int) -> TokenResponse:
        expire = datetime.utcnow() + timedelta(minutes=15)
        payload = {"sub": str(user_id), "exp": expire}
        token = jwt.encode(payload, self.ACCESS_SECRET, self.ALGORITHM)
        return TokenResponse(access_token=token)
