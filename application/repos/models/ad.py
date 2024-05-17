from decimal import Decimal
from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey, String, text, types, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from application.domain.entities.ad import Advertisement as DomainAdvertisement
from application.domain.value_objects.ad import Status, Photo
from application.infrastructure.database import Base


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
    number_of_views: Mapped[int]
    photo: Mapped[list] = mapped_column(JSON)
    status: Mapped[str]
    author_id: Mapped[UUID] = mapped_column(ForeignKey(column="user.oid", ondelete="CASCADE"))
    category_id: Mapped[UUID] = mapped_column(ForeignKey(column="category.oid", ondelete="CASCADE"))

    user = relationship("User", back_populates="advertisements", lazy="selectin")
    category = relationship("Category", back_populates="advertisements", lazy="selectin")
    moderation = relationship("Moderation", back_populates="advertisement", lazy="selectin")

    @classmethod
    def from_entity(cls, advertisement: DomainAdvertisement) -> "Advertisement":
        return cls(
                oid=advertisement.oid,
                title=advertisement.title,
                city=advertisement.city,
                description=advertisement.description,
                created_at=advertisement.created_at,
                approved_at=advertisement.approved_at,
                price=advertisement.price,
                number_of_views=advertisement.number_of_views,
                photo=advertisement.photo.value,
                status=advertisement.status.name,
                author_id=advertisement.author.oid,
                category_id=advertisement.category.oid
            )

    def to_entity(self) -> DomainAdvertisement:
        return DomainAdvertisement(
            oid=str(self.oid),
            title=self.title,
            city=self.city,
            description=self.description,
            created_at=self.created_at,
            approved_at=self.approved_at,
            price=self.price,
            number_of_views=self.number_of_views,
            photo=Photo(self.photo),
            status=Status[self.status],
            author=self.user.to_entity(),
            category=self.category.to_entity()
        )

    @staticmethod
    def to_dict(advertisement: DomainAdvertisement) -> dict[str, str]:
        return {
            "oid": advertisement.oid,
            "title": advertisement.title,
            "city": advertisement.city,
            "description": advertisement.description,
            "created_at": advertisement.created_at,
            "approved_at": advertisement.approved_at,
            "price": advertisement.price,
            "number_of_views": advertisement.number_of_views,
            "photo": advertisement.photo.value,
            "status": advertisement.status.name,
            "author_id": advertisement.author.oid,
            "category_id": advertisement.category.oid
        }

