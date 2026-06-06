"""Auth schemas — registration, login, token responses."""

from pydantic import BaseModel, EmailStr, Field
from app.models.user import UserRole


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    role: UserRole = UserRole.STUDENT
    name: str = Field(..., min_length=1, max_length=255)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    role: UserRole


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class GoogleOAuthRequest(BaseModel):
    """Google OAuth token received from frontend Google Sign-In."""
    credential: str = Field(..., description="Google ID token from the frontend")


class MessageResponse(BaseModel):
    message: str
