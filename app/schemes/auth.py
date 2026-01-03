from pydantic import BaseModel, EmailStr, Field, validator


class TokenResponse(BaseModel):
    access_token: str

class Token(BaseModel):
    token: str

class Login(BaseModel):
    email: EmailStr
    password: str

    @validator("password")
    def password_complexity(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str