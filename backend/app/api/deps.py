from typing import Annotated

from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.exceptions import UnauthorizedException, ForbiddenException
from app.core.security import verify_token
from app.db.session import get_async_session
from app.models.user import User, UserRole


async def get_db() -> AsyncSession:
    """Provide an async database session."""
    async for session in get_async_session():
        yield session


async def get_current_user(
    authorization: str = Header(..., description="Bearer <token>"),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Extract and verify JWT from Authorization header, return current user."""
    if not authorization.startswith("Bearer "):
        raise UnauthorizedException("Invalid authorization header format")

    token = authorization.replace("Bearer ", "")
    
    # Check if token is blacklisted
    try:
        from app.core.config import settings
        import redis.asyncio as redis
        
        r = redis.from_url(settings.REDIS_URL)
        is_blacklisted = await r.get(f"blacklist:{token}")
        await r.aclose()
        
        if is_blacklisted:
            raise UnauthorizedException("Token has been revoked")
    except Exception:
        # Redis not available - skip blacklist check
        pass
    
    payload = verify_token(token, token_type="access")
    if payload is None:
        raise UnauthorizedException("Invalid or expired token")

    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedException("Invalid token payload")

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user or not user.is_active:
        raise UnauthorizedException("User not found or inactive")

    return user


def require_role(*roles: UserRole):
    """Factory that returns a dependency requiring specific user roles."""
    async def role_checker(
        current_user: User = Depends(get_current_user),
    ) -> User:
        if current_user.role not in roles:
            raise ForbiddenException(
                f"Role '{current_user.role.value}' not authorized. Required: {[r.value for r in roles]}"
            )
        return current_user
    return role_checker


# Typed dependencies for cleaner route signatures
DBSession = Annotated[AsyncSession, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]
