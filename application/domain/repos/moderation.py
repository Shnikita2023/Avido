from abc import ABC, abstractmethod

from application.domain.entities.moderation import Moderation as DomainModeration


class AbstractModerationRepository(ABC):

    @abstractmethod
    async def add(self, moderation: DomainModeration) -> DomainModeration:
        raise NotImplemented

    @abstractmethod
    async def get(self, moderation_oid: str) -> DomainModeration | None:
        raise NotImplemented
