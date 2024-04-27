from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.db.base import Base


class Decision(Enum):
    PUBLISH = "Опубликовать"
    MODIFICATION = "Отправить на доработку"


class Moderation(Base):
    __tablename__ = "moderation"

    moderation_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    decision: Mapped[Decision]
    rejection_reason: Mapped[str]

    user_id: Mapped[int] = mapped_column(ForeignKey(column="user.id", ondelete="CASCADE"), unique=True)
    user: Mapped["User"] = relationship(back_populates="moderations")

    advertisement_id: Mapped[int] = mapped_column(
        ForeignKey(column="advertisement.id", ondelete="CASCADE"),
        unique=True,
    )

    advertisement: Mapped["Advertisement"] = relationship(back_populates="moderation")
