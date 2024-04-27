from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.db.base import Base


class Category(Base):
    __tablename__ = "category"

    title: Mapped[str] = mapped_column(String(50))
    code: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    description: Mapped[str] = mapped_column(String(250))
    sort_order: Mapped[int]

    advertisements: Mapped["Advertisement"] = relationship(back_populates="category")

    def __str__(self):
        return f"Категория объявление {self.title}"
