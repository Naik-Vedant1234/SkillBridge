"""Auth endpoints - registration, login, logout, refresh, Google OAuth."""

from fastapi import APIRouter, Depends, Header, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import DBSession
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    RefreshTokenRequest,
    GoogleOAuthRequest,
    MessageResponse,
)
from app.services.auth_service import (
    register_user,
    login_user,
    refresh_access_token,
)
from app.services.oauth_service import oauth_service

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
async def logout(
    authorization: str = Header(None, description="Bearer <token>"),
):
    """
    Logout endpoint with optional token blacklisting.
    
    If Redis is available, blacklist the token until expiration.
    Otherwise, client-side token deletion is sufficient.
    """
    if authorization and authorization.startswith("Bearer "):
        token = authorization.replace("Bearer ", "")
        
        try:
            # Try to blacklist token in Redis
            from app.core.config import settings
            import redis.asyncio as redis
            from app.core.security import verify_token
            
            # Verify token and get expiry
            payload = verify_token(token, token_type="access")
            if payload:
                r = redis.from_url(settings.REDIS_URL)
                
                # Calculate remaining TTL
                from datetime import datetime, timezone
                exp_timestamp = payload.get("exp")
                if exp_timestamp:
                    now = datetime.now(timezone.utc).timestamp()
                    ttl = int(exp_timestamp - now)
                    
                    if ttl > 0:
                        # Blacklist token with remaining TTL
                        await r.setex(f"blacklist:{token}", ttl, "1")
                
                await r.aclose()
        except Exception as e:
            # Redis not available or error - continue with client-side logout
            print(f"Token blacklist error (non-critical): {str(e)}")
    
    return MessageResponse(
        message="Logged out successfully. Please delete your tokens."
    )


@router.post("/google", response_model=TokenResponse)
async def google_oauth(
    oauth_data: GoogleOAuthRequest,
    db: DBSession,
):
    """
    Google OAuth callback endpoint.
    
    Process:
    1. Exchange authorization code for access token
    2. Get user info from Google
    3. Create or authenticate user
    4. Return JWT tokens
    
    The frontend should:
    1. Redirect user to Google OAuth consent screen
    2. Receive authorization code in callback
    3. Send code and redirect_uri to this endpoint
    4. Store returned JWT tokens
    """
    # Exchange code for Google access token
    token_data = await oauth_service.exchange_code_for_token(
        code=oauth_data.code,
        redirect_uri=oauth_data.redirect_uri,
    )
    
    # Get user info from Google
    user_info = await oauth_service.get_user_info(
        access_token=token_data["access_token"]
    )
    
    # Authenticate or create user
    return await oauth_service.authenticate_or_create_user(
        google_user_info=user_info,
        role=oauth_data.role,
        db=db,
    )
