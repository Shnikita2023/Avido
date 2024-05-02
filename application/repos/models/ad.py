from decimal import Decimal
from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey, String, text, types
from sqlalchemy.orm import Mapped, mapped_column, relationship

from application.infrastructure.base import Base


class Advertisement(Base):
    __tablename__ = "advertisement"

    oid: Mapped[UUID] = mapped_column(types.Uuid,
                                      primary_key=True,
                                      server_default=text("gen_random_uuid()"))
    title: Mapped[str] = mapped_column(String(50))
    city: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(250))
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    approved_at: Mapped[datetime | None] = mapped_column(default=None)
    price: Mapped[Decimal]
    number_views: Mapped[int]
    photo: Mapped[str]
    status: Mapped[str]
    created_by: Mapped[int] = mapped_column(ForeignKey(column="user.oid", ondelete="CASCADE"))
    category_oid: Mapped[int] = mapped_column(ForeignKey(column="category.oid", ondelete="CASCADE"))

    user = relationship("User", back_populates="advertisements")
    category = relationship("Category", back_populates="advertisements")
    moderation = relationship("Moderation", back_populates="advertisement", uselist=False)

