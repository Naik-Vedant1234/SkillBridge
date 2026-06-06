"""Auth service - handles authentication business logic."""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.user import User, UserRole
from app.models.student import Student
from app.models.mentor import Mentor
from app.models.company import Company
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_token,
)
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse


async def register_user(
    register_data: RegisterRequest,
    db: AsyncSession,
) -> TokenResponse:
    """Register a new user and create their profile."""
    
    # Check if email already exists
    result = await db.execute(select(User).where(User.email == register_data.email))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    user = User(
        email=register_data.email,
        password_hash=hash_password(register_data.password),
        role=register_data.role,
        is_active=True,
    )
    db.add(user)
    await db.flush()  # Get user.id without committing
    
    # Create role-specific profile
    if register_data.role == UserRole.STUDENT:
        profile = Student(user_id=user.id, name=register_data.name)
        db.add(profile)
    elif register_data.role == UserRole.MENTOR:
        profile = Mentor(user_id=user.id, name=register_data.name)
        db.add(profile)
    elif register_data.role == UserRole.COMPANY:
        profile = Company(user_id=user.id, name=register_data.name)
        db.add(profile)
    
    await db.commit()
    
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


async def login_user(
    login_data: LoginRequest,
    db: AsyncSession,
) -> TokenResponse:
    """Authenticate user and return tokens."""
    
    # Find user by email
    result = await db.execute(select(User).where(User.email == login_data.email))
    user = result.scalar_one_or_none()
    
    if not user or not user.password_hash:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Verify password
    if not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Check if account is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )
    
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


async def refresh_access_token(
    refresh_token: str,
    db: AsyncSession,
) -> TokenResponse:
    """Generate new access token from refresh token."""
    
    # Verify refresh token
    payload = verify_token(refresh_token, token_type="refresh")
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )
    
    # Get user
    user_id = payload.get("sub")
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    # Generate new tokens
    access_token = create_access_token(
        subject=str(user.id),
        extra_claims={"role": user.role.value}
    )
    new_refresh_token = create_refresh_token(subject=str(user.id))
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=new_refresh_token,
        role=user.role
    )
