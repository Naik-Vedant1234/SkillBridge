"""Auth endpoints - registration, login, logout, refresh."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import DBSession
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    RefreshTokenRequest,
    MessageResponse,
)
from app.services.auth_service import (
    register_user,
    login_user,
    refresh_access_token,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    register_data: RegisterRequest,
    db: DBSession,
):
    """
    Register a new user account.
    
    Creates a user with the specified role and automatically creates
    the corresponding profile (Student, Mentor, or Company).
    
    Returns JWT access and refresh tokens upon successful registration.
    """
    return await register_user(register_data, db)


@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: LoginRequest,
    db: DBSession,
):
    """
    Login with email and password.
    
    Returns JWT access and refresh tokens upon successful authentication.
    Access tokens expire in 30 minutes, refresh tokens in 7 days.
    """
    return await login_user(login_data, db)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    db: DBSession,
):
    """
    Refresh access token using refresh token.
    
    Provides a new access token and refresh token pair.
    Use this endpoint when the access token expires.
    """
    return await refresh_access_token(refresh_data.refresh_token, db)


@router.post("/logout", response_model=MessageResponse)
async def logout():
    """
    Logout endpoint (client-side token deletion).
    
    Since we're using stateless JWT tokens, logout is handled
    client-side by deleting the stored tokens.
    
    For server-side logout, implement token blacklisting with Redis.
    """
    return MessageResponse(message="Logged out successfully. Please delete your tokens.")


@router.post("/google", response_model=TokenResponse, status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def google_oauth():
    """
    Google OAuth login (to be implemented in Phase 3).
    
    Will accept Google ID token from frontend Google Sign-In
    and create/login user account.
    """
    return MessageResponse(message="Google OAuth - to be implemented in Phase 3")
