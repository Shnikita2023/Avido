import bcrypt
from uuid import uuid4

from pydantic import Field as f

from .base import BaseEntity
from ..value_objects.user import Email, Password, Phone, FullName, Role, Status
from application.web.views.user.schemas import UserOutput, UserInput


class User(BaseEntity):
    first_name: FullName = f(title="Имя")
    last_name: FullName = f(title="Фамилия")
    middle_name: FullName | None = f(title="Отчество", default=None)
    email: Email = f(title="Email")
    password: Password = f(title="Пароль")
    role: Role = f(title="Роль", default=Role.USER)
    number_phone: Phone = f(title="Номер телефона")
    time_call: str | None = f(
        title="Время звонка",
        description="Когда удобно принимать звонки",
        default=None,
        max_length=50
    )
    status: Status = f(title="Статус", default=Status.PENDING)

    @classmethod
    def from_json(cls, json: dict) -> "User":
        return cls(
            first_name=FullName(json["first_name"]),
            last_name=FullName(json["last_name"]),
            middle_name=FullName(json["middle_name"]),
            email=Email(schema.email),
            password=Password("FakePassw0rd!123" if isinstance(schema, UserOutput) else schema.password),
            number_phone=Phone(schema.number_phone),
            time_call=schema.time_call,
            oid=schema.oid if isinstance(schema, UserOutput) else str(uuid4())
        )

    def to_json(self) -> dict:
        return self.model_dump(mode="python")

    def encrypt_password(self):
        salt: bytes = bcrypt.gensalt()
        pwd_bytes: bytes = self.password.encode()
        self.password: bytes = bcrypt.hashpw(pwd_bytes, salt)

    def is_password_valid(self, password: str):
        return bcrypt.checkpw(password=password.encode(), hashed_password=self.password)

