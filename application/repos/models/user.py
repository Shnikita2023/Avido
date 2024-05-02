from uuid import UUID

from sqlalchemy import String, text, types
from sqlalchemy.orm import Mapped, mapped_column, relationship

from application.domain.entities.user import User as DomainUser, Role, Status
from application.infrastructure.base import Base


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

    advertisements = relationship("Advertisement", back_populates="user")
    moderations = relationship("Moderation", back_populates="user")

    def to_entity(self) -> DomainUser:
        return DomainUser(
            oid=self.oid,
            first_name=self.first_name,
            last_name=self.last_name,
            middle_name=self.middle_name,
            email=self.email,
            role=Role[self.role],
            number_phone=self.number_phone,
            time_call=self.time_call,
            status=Status[self.status]
        )

    @staticmethod
    def to_dict(user: DomainUser) -> dict[str, str]:
        return {
            "guid": user.oid,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "middle_name": user.middle_name,
            "email": user.email,
            "role": user.role,
            "number_phone": user.number_phone,
            "time_call": user.time_call,
            "status": user.status
        }
