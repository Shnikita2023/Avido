from typing import Optional
from uuid import UUID

from sqlalchemy import select, Result
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from application.domain.entities.moderation import Moderation as DomainModeration
from application.domain.repos.moderation import AbstractModerationRepository
from application.exceptions.db import DBError
from application.repos.models import Moderation


class SQLAlchemyModerationRepository(AbstractModerationRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, moderation: DomainModeration) -> DomainModeration:
        try:
            moderation_model: Moderation = Moderation.from_entity(moderation)
            self.session.add(moderation_model)
            return moderation

        except SQLAlchemyError as exc:
            raise DBError(exc)

    async def get(self, moderation_oid: str) -> DomainModeration | None:
        try:
            query = select(Moderation).where(Moderation.oid == moderation_oid)
            result: Result = await self.session.execute(query)
            advertisement_model: Optional[Moderation] = result.scalar_one_or_none()
            if advertisement_model:
                return advertisement_model.to_entity()

        except SQLAlchemyError as exc:
            raise DBError(exc)
