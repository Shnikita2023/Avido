import bcrypt
from uuid import uuid4

from pydantic import Field as f

from .base import BaseEntity
from ..value_objects.user import Email, Password, Phone, FullName, Role, Status


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
    def from_json(cls, json: dict[str, str]) -> "User":
        return cls(
            first_name=FullName(json["first_name"]),
            last_name=FullName(json["last_name"]),
            middle_name=FullName(json["middle_name"]),
            email=Email(json["email"]),
            password=Password(json["password"] if json.get("password") else "FakePassw0rd!123"),
            number_phone=Phone(json["number_phone"]),
            time_call=json["time_call"],
            oid=json["oid"] if json.get("oid") else str(uuid4())
        )

    def to_json(self) -> dict:
        return self.model_dump(exclude={"password"})

    def encrypt_password(self) -> None:
        salt: bytes = bcrypt.gensalt()
        pwd_bytes: bytes = self.password.value.encode()
        self.password: bytes = bcrypt.hashpw(pwd_bytes, salt)

    def is_password_valid(self, password: str) -> bool:
        return bcrypt.checkpw(password=password.encode(), hashed_password=self.password.value.encode())

