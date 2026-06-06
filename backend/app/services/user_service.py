"""User service — user profile management."""


class UserService:
    """Business logic for user management."""

    async def get_user_by_id(self, user_id: str) -> dict:
        raise NotImplementedError("To be implemented in Phase 2")

    async def update_user(self, user_id: str, data: dict) -> dict:
        raise NotImplementedError("To be implemented in Phase 2")
