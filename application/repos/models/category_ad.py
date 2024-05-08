from uuid import UUID

from sqlalchemy import String, text, types
from sqlalchemy.orm import Mapped, mapped_column, relationship

from application.domain.category_ad.category_ad import Category as DomainCategory
from application.infrastructure.database import Base


class Category(Base):
    __tablename__ = "category"

    oid: Mapped[UUID] = mapped_column(types.Uuid,
                                      primary_key=True,
                                      server_default=text("gen_random_uuid()"))
    title: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    description: Mapped[str] = mapped_column(String(250))

    advertisements = relationship("Advertisement", back_populates="category")

    @classmethod
    def from_entity(cls, category_ad: DomainCategory) -> "Category":
        return cls(
            oid=category_ad.oid,
            title=category_ad.title,
            code=category_ad.code,
            description=category_ad.description
        )

    def to_entity(self) -> DomainCategory:
        return DomainCategory(
            oid=self.oid,
            title=self.title,
            code=self.code,
            description=self.description,
        )
