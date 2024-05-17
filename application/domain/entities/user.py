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
    def to_entity(cls, schema: UserOutput | UserInput) -> "User":
        return cls(
            first_name=FullName(schema.first_name),
            last_name=FullName(schema.last_name),
            middle_name=FullName(schema.middle_name),
            email=Email(schema.email),
            password=Password("FakePassw0rd!123" if isinstance(schema, UserOutput) else schema.password),
            number_phone=Phone(schema.number_phone),
            time_call=schema.time_call,
            oid=schema.oid if isinstance(schema, UserOutput) else str(uuid4())
        )

    def to_schema(self) -> UserOutput:
        return UserOutput(
            oid=self.oid,
            first_name=self.first_name.value,
            last_name=self.last_name.value,
            middle_name=self.middle_name.value,
            email=self.email.value,
            number_phone=self.number_phone.value,
            time_call=self.time_call,
            role=self.role.name,
            status=self.status.value
        )
