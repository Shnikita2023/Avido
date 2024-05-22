from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import ForeignKey, text, types
from sqlalchemy.orm import Mapped, mapped_column, relationship

from application.domain.entities.moderation import Moderation as DomainModeration
from application.infrastructure.database import Base


class Moderation(Base):
    __tablename__ = "moderation"

    oid: Mapped[UUID] = mapped_column(types.Uuid,
                                      primary_key=True,
                                      server_default=text("gen_random_uuid()"))
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    is_approved: Mapped[bool]
    rejection_reason: Mapped[str]

    moderator_id: Mapped[UUID] = mapped_column(ForeignKey(column="user.oid", ondelete="CASCADE"))
    advertisement_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey(column="advertisement.oid", ondelete="SET NULL"))

    user = relationship("User", back_populates="moderations", lazy="selectin")
    advertisement = relationship("Advertisement", back_populates="moderation")

    @classmethod
    def from_entity(cls, moderation: DomainModeration) -> "Moderation":
        return cls(
            oid=moderation.oid,
            created_at=moderation.created_at,
            is_approved=moderation.is_approved,
            rejection_reason=moderation.rejection_reason,
            moderator_id=moderation.moderator_id,
            advertisement_id=moderation.advertisement_id,
        )

    def to_entity(self) -> DomainModeration:
        return DomainModeration(
            oid=str(self.oid),
            created_at=self.created_at,
            is_approved=self.is_approved,
            rejection_reason=self.rejection_reason,
            advertisement_id=str(self.advertisement_id),
            moderator_id=str(self.moderator_id)
        )
