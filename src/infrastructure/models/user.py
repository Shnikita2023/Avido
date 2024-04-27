from enum import Enum

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.db.base import Base


class StatusUser(Enum):
    ACTIVE = "Активный"
    BLOCKED = "Заблокирован"
    PENDING = "Ожидает подтверждение email"


class Role(Enum):
    ADMIN = "Администратор"
    GUEST = "Гость"
    USER = "Пользователь"
    MODERATOR = "Модератор"


class User(Base):
    __tablename__ = "user"

    name: Mapped[str] = mapped_column(String(50))
    surname: Mapped[str] = mapped_column(String(50))
    middle_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    role: Mapped[Role]
    number_phone: Mapped[str] = mapped_column(String(11), unique=True, index=True)
    time_of_the_call: Mapped[str] = mapped_column(String(50))
    status_user: Mapped[StatusUser]

    advertisements: Mapped["Advertisement"] = relationship(back_populates="user")
    moderations: Mapped["Moderation"] = relationship(back_populates="user")

    def __str__(self):
        return f"Пользователь {self.name}"
