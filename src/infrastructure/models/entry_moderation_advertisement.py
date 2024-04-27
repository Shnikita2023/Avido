from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.db.base import Base


# class Decision(Enum):
#     PUBLISH = "Опубликовать"
#     MODIFICATION = "Отправить на доработку"


class Moderation(Base):
    __tablename__ = "moderation"

    moderation_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    is_approved: Mapped[bool]
    rejection_reason: Mapped[str]

    moderated_by: Mapped[int] = mapped_column(ForeignKey(column="user.id", ondelete="CASCADE"))
    user: Mapped["User"] = relationship(back_populates="moderations")

    advertisement_id: Mapped[int] = mapped_column(
        ForeignKey(column="advertisement.id", ondelete="CASCADE"),
        unique=True,
    )

    advertisement: Mapped["Advertisement"] = relationship(back_populates="moderation")
