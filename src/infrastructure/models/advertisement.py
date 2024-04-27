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
    date_publication: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    price: Mapped[float]
    number_of_views: Mapped[int]
    photo: Mapped[str]
    status_ad: Mapped[StatusAd]

    user_id: Mapped[int] = mapped_column(ForeignKey(column="user.id", ondelete="CASCADE"), unique=True)
    user: Mapped["User"] = relationship(back_populates="advertisements")

    category_id: Mapped[int] = mapped_column(ForeignKey(column="category.id", ondelete="CASCADE"), unique=True)
    category: Mapped["Category"] = relationship(back_populates="advertisements")

    moderation: Mapped["Moderation"] = relationship(back_populates="advertisement", uselist=False)

    def __str__(self):
        return f"Объявление {self.title}"
