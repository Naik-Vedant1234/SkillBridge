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
    """Google OAuth callback request."""
    code: str = Field(..., description="Authorization code from Google OAuth")
    redirect_uri: str = Field(..., description="Redirect URI used in OAuth flow")
    role: UserRole = Field(default=UserRole.STUDENT, description="Role for new user creation")


class MessageResponse(BaseModel):
    message: str
