from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey, text, types
from sqlalchemy.orm import Mapped, mapped_column, relationship

from application.infrastructure.base import Base


class Moderation(Base):
    __tablename__ = "moderation"

    oid: Mapped[UUID] = mapped_column(types.Uuid,
                                      primary_key=True,
                                      server_default=text("gen_random_uuid()"))
    moderation_date: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    is_approved: Mapped[bool]
    rejection_reason: Mapped[str]

    moderated_by: Mapped[int] = mapped_column(ForeignKey(column="user.oid", ondelete="CASCADE"))
    advertisement_oid: Mapped[int] = mapped_column(
        ForeignKey(column="advertisement.oid", ondelete="CASCADE"),
        unique=True,
    )

    user = relationship("User", back_populates="moderations")
    advertisement = relationship("Advertisement", back_populates="moderation")
