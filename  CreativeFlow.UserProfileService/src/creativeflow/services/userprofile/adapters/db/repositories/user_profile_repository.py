"""
SQLAlchemy repository for UserProfile data.
"""
from datetime import datetime
from typing import List, Optional

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from ....domain.models import Preferences, UserProfile
from ....domain.repositories import IUserProfileRepository
from ..sqlalchemy_models import UserProfileSQL


class SQLAlchemyUserProfileRepository(IUserProfileRepository):
    """
    Handles database operations (CRUD) for UserProfile domain entities
    using SQLAlchemy's async session.
    """

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    def _to_domain(self, orm_user: UserProfileSQL) -> UserProfile:
        """Maps an ORM object to a domain model."""
        return UserProfile(
            id=orm_user.id,
            auth_user_id=orm_user.auth_user_id,
            full_name=orm_user.full_name,
            username=orm_user.username,
            profile_picture_url=orm_user.profile_picture_url,
            preferences=Preferences(
                language_preference=orm_user.language_preference,
                timezone=orm_user.timezone,
                ui_settings=orm_user.ui_settings or {},
            ),
            created_at=orm_user.created_at,
            updated_at=orm_user.updated_at,
            last_activity_at=orm_user.last_activity_at,
            is_anonymized=orm_user.is_anonymized,
        )

    async def get_by_auth_id(self, auth_user_id: str) -> Optional[UserProfile]:
        stmt = select(UserProfileSQL).where(UserProfileSQL.auth_user_id == auth_user_id)
        result = await self.db_session.execute(stmt)
        orm_user = result.scalars().first()
        return self._to_domain(orm_user) if orm_user else None

    async def save(self, user_profile: UserProfile) -> UserProfile:
        stmt = select(UserProfileSQL).where(UserProfileSQL.id == user_profile.id)
        result = await self.db_session.execute(stmt)
        orm_user = result.scalars().first()

        if orm_user:
            # Update existing user
            orm_user.full_name = user_profile.full_name
            orm_user.username = user_profile.username
            orm_user.profile_picture_url = str(user_profile.profile_picture_url) if user_profile.profile_picture_url else None
            orm_user.language_preference = user_profile.preferences.language_preference
            orm_user.timezone = user_profile.preferences.timezone
            orm_user.ui_settings = user_profile.preferences.ui_settings
            orm_user.updated_at = user_profile.updated_at
            orm_user.last_activity_at = user_profile.last_activity_at
            orm_user.is_anonymized = user_profile.is_anonymized
        else:
            # Create new user
            orm_user = UserProfileSQL(
                id=user_profile.id,
                auth_user_id=user_profile.auth_user_id,
                full_name=user_profile.full_name,
                username=user_profile.username,
                profile_picture_url=str(user_profile.profile_picture_url) if user_profile.profile_picture_url else None,
                language_preference=user_profile.preferences.language_preference,
                timezone=user_profile.preferences.timezone,
                ui_settings=user_profile.preferences.ui_settings,
                created_at=user_profile.created_at,
                updated_at=user_profile.updated_at,
                last_activity_at=user_profile.last_activity_at,
                is_anonymized=user_profile.is_anonymized,
            )
            self.db_session.add(orm_user)
        
        await self.db_session.commit()
        await self.db_session.refresh(orm_user)
        return self._to_domain(orm_user)

    async def delete_by_auth_id(self, auth_user_id: str) -> None:
        stmt = delete(UserProfileSQL).where(UserProfileSQL.auth_user_id == auth_user_id)
        await self.db_session.execute(stmt)
        await self.db_session.commit()

    async def get_profiles_for_retention_check(
        self, last_activity_before: datetime, is_anonymized: bool = False
    ) -> List[UserProfile]:
        stmt = select(UserProfileSQL).where(
            UserProfileSQL.last_activity_at < last_activity_before,
            UserProfileSQL.is_anonymized == is_anonymized
        )
        result = await self.db_session.execute(stmt)
        orm_users = result.scalars().all()
        return [self._to_domain(user) for user in orm_users]