from uuid import UUID

from sqlalchemy import String, text, types
from sqlalchemy.orm import Mapped, mapped_column, relationship

from application.infrastructure.database import Base


class Category(Base):
    __tablename__ = "category"

    oid: Mapped[UUID] = mapped_column(types.Uuid,
                                      primary_key=True,
                                      server_default=text("gen_random_uuid()"))
    title: Mapped[str] = mapped_column(String(50))
    code: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    description: Mapped[str] = mapped_column(String(250))

    advertisements = relationship("Advertisement", back_populates="category")
