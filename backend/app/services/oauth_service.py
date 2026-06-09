"""Google OAuth service for authentication."""

import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.models.user import User, UserRole
from app.models.student import Student
from app.models.mentor import Mentor
from app.models.company import Company
from app.core.config import settings
from app.core.security import create_access_token, create_refresh_token
from app.schemas.auth import TokenResponse


class GoogleOAuthService:
    """Handle Google OAuth authentication flow."""
    
    GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
    GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"
    
    @staticmethod
    async def exchange_code_for_token(code: str, redirect_uri: str) -> dict:
        """
        Exchange authorization code for access token.
        
        Args:
            code: Authorization code from Google OAuth callback
            redirect_uri: Redirect URI used in the OAuth flow
            
        Returns:
            dict with access_token, token_type, expires_in, etc.
            
        Raises:
            HTTPException: If token exchange fails
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                GoogleOAuthService.GOOGLE_TOKEN_URL,
                data={
                    "code": code,
                    "client_id": settings.GOOGLE_CLIENT_ID,
                    "client_secret": settings.GOOGLE_CLIENT_SECRET,
                    "redirect_uri": redirect_uri,
                    "grant_type": "authorization_code",
                },
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=400,
                    detail=f"Failed to exchange code for token: {response.text}"
                )
            
            return response.json()
    
    @staticmethod
    async def get_user_info(access_token: str) -> dict:
        """
        Get user information from Google using access token.
        
        Args:
            access_token: Google OAuth access token
            
        Returns:
            dict with id, email, verified_email, name, picture, etc.
            
        Raises:
            HTTPException: If user info request fails
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                GoogleOAuthService.GOOGLE_USERINFO_URL,
                headers={"Authorization": f"Bearer {access_token}"},
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=400,
                    detail=f"Failed to get user info: {response.text}"
                )
            
            return response.json()
    
    @staticmethod
    async def authenticate_or_create_user(
        google_user_info: dict,
        role: UserRole,
        db: AsyncSession,
    ) -> TokenResponse:
        """
        Authenticate existing user or create new user from Google OAuth.
        
        Process:
        1. Check if user exists by google_id or email
        2. If exists, update google_id if needed and return tokens
        3. If not exists, create User + role-specific profile
        4. Generate JWT tokens
        
        Args:
            google_user_info: User info from Google (id, email, name, picture)
            role: UserRole for new user creation
            db: Database session
            
        Returns:
            TokenResponse with access_token, refresh_token, role
        """
        google_id = google_user_info.get("id")
        email = google_user_info.get("email")
        name = google_user_info.get("name", email.split("@")[0])
        avatar_url = google_user_info.get("picture")
        
        if not google_id or not email:
            raise HTTPException(
                status_code=400,
                detail="Invalid Google user info: missing id or email"
            )
        
        # Check if user exists by google_id
        result = await db.execute(
            select(User).where(User.google_id == google_id)
        )
        user = result.scalar_one_or_none()
        
        if user:
            # User exists, return tokens
            access_token = create_access_token(
                subject=str(user.id),
                extra_claims={"role": user.role.value}
            )
            refresh_token = create_refresh_token(subject=str(user.id))
            
            return TokenResponse(
                access_token=access_token,
                refresh_token=refresh_token,
                role=user.role
            )
        
        # Check if user exists by email (might have registered with password)
        result = await db.execute(
            select(User).where(User.email == email)
        )
        user = result.scalar_one_or_none()
        
        if user:
            # Link Google account to existing user
            user.google_id = google_id
            await db.commit()
            
            access_token = create_access_token(
                subject=str(user.id),
                extra_claims={"role": user.role.value}
            )
            refresh_token = create_refresh_token(subject=str(user.id))
            
            return TokenResponse(
                access_token=access_token,
                refresh_token=refresh_token,
                role=user.role
            )
        
        # Create new user
        user = User(
            email=email,
            google_id=google_id,
            role=role,
            is_active=True,
            password_hash=None,  # Google OAuth users don't have password
        )
        db.add(user)
        await db.flush()
        
        # Create profile based on role
        if role == UserRole.STUDENT:
            profile = Student(
                user_id=user.id,
                name=name,
                avatar_url=avatar_url,
            )
        elif role == UserRole.MENTOR:
            profile = Mentor(
                user_id=user.id,
                name=name,
            )
        elif role == UserRole.COMPANY:
            profile = Company(
                user_id=user.id,
                name=name,
                logo_url=avatar_url,
            )
        else:
            # Admin role shouldn't be created via OAuth
            await db.rollback()
            raise HTTPException(
                status_code=403,
                detail="Cannot create admin accounts via Google OAuth"
            )
        
        db.add(profile)
        await db.commit()
        await db.refresh(user)
        
        # Generate tokens
        access_token = create_access_token(
            subject=str(user.id),
            extra_claims={"role": user.role.value}
        )
        refresh_token = create_refresh_token(subject=str(user.id))
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            role=user.role
        )


oauth_service = GoogleOAuthService()
