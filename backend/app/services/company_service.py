"""Company service — company profile management."""

import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.company import Company
from app.schemas.company import CompanyUpdate


class CompanyService:
    """Business logic for company profile management."""

    async def get_company_by_user_id(
        self, db: AsyncSession, user_id: uuid.UUID
    ) -> Company | None:
        """Get company profile by user ID."""
        result = await db.execute(select(Company).where(Company.user_id == user_id))
        return result.scalar_one_or_none()

    async def update_company_profile(
        self, db: AsyncSession, company_id: uuid.UUID, data: CompanyUpdate
    ) -> Company:
        """Update company profile fields."""
        result = await db.execute(select(Company).where(Company.id == company_id))
        company = result.scalar_one_or_none()
        if not company:
            raise ValueError("Company not found")

        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(company, field, value)

        await db.commit()
        await db.refresh(company)
        return company
