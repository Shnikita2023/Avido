from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.db.base import Base


class StatusAd(Enum):
    DRAFT = "Черновик"
    ON_MODERATION = "На модерации"
    REJECTED_FOR_REVISION = "Отклонено, к доработке"
    REMOVED = "Снято/Продано"
    ACTIVE = "Опубликована"


class Advertisement(Base):
    __tablename__ = "advertisement"

    title: Mapped[str] = mapped_column(String(50))
    city: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(250))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    approved_at: Mapped[datetime] | None = mapped_column(DateTime(timezone=True))
    price: Mapped[float]
    number_of_views: Mapped[int]
    photo: Mapped[list[str]]
    status: Mapped[str]
    created_by: Mapped[int] = mapped_column(ForeignKey(column="user.id", ondelete="CASCADE"))
    category_id: Mapped[int] = mapped_column(ForeignKey(column="category.id", ondelete="CASCADE"))

    user: Mapped["User"] = relationship(back_populates="advertisements")
    category: Mapped["Category"] = relationship(back_populates="advertisements")
    moderation: Mapped["Moderation"] = relationship(back_populates="advertisement", uselist=False)

    def __str__(self):
        return f"Объявление {self.title}"
