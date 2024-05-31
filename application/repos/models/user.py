from datetime import datetime
from uuid import UUID

from sqlalchemy import String, text, types
from sqlalchemy.orm import Mapped, mapped_column, relationship

from application.domain.entities.user import User as DomainUser
from application.domain.value_objects.user import FullName, Phone, Email, Role, Status
from . import Base


class User(Base):
    __tablename__ = "user"

    oid: Mapped[UUID] = mapped_column(types.Uuid,
                                      primary_key=True,
                                      server_default=text("gen_random_uuid()"))
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    middle_name: Mapped[str | None] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    role: Mapped[str]
    number_phone: Mapped[str] = mapped_column(String(11), unique=True, index=True)
    time_call: Mapped[str] = mapped_column(String(50))
    status: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))

    advertisements = relationship("Advertisement", back_populates="user")
    moderations = relationship("Moderation", back_populates="user")

    def to_entity(self) -> DomainUser:
        return DomainUser(
            oid=str(self.oid),
            first_name=FullName(self.first_name),
            last_name=FullName(self.last_name),
            middle_name=FullName(self.middle_name),
            email=Email(self.email),
            number_phone=Phone(self.number_phone),
            role=Role[self.role],
            time_call=self.time_call,
            status=Status[self.status],
            created_at=self.created_at
        )

    @classmethod
    def from_entity(cls, user: DomainUser) -> "User":
        return cls(
            oid=user.oid,
            first_name=user.first_name.value,
            last_name=user.last_name.value,
            middle_name=user.middle_name.value,
            email=user.email.value,
            role=user.role.name,
            number_phone=user.number_phone.value,
            time_call=user.time_call,
            status=user.status.name,
            created_at=user.created_at
        )

    @staticmethod
    def to_dict(user: DomainUser) -> dict[str, str]:
        return {
            "oid": user.oid,
            "first_name": user.first_name.value,
            "last_name": user.last_name.value,
            "middle_name": user.middle_name.value,
            "email": user.email.value,
            "role": user.role.name,
            "number_phone": user.number_phone.value,
            "time_call": user.time_call,
            "status": user.status.name
        }
