import uuid

from pydantic import BaseModel, ConfigDict, EmailStr

from pydantic import Field as f

from application.domain.entities.user import User as DomainUser, User


class UserInput(BaseModel):
    model_config = ConfigDict(strict=True)

    first_name: str = f(title="Имя")
    last_name: str = f(title="Фамилия")
    middle_name: str | None = f(default=None, title="Отчество")
    email: EmailStr = f(title="Емайл")
    number_phone: str = f(title="Номер телефона")
    time_call: str = f(
        title="Время звонка",
        description="Когда удобно принимать звонки",
        min_length=1,
        max_length=50
    )


UserOutput = User

# class UserOutput(UserInput):
#     user_id: uuid.UUID
#
#     @staticmethod
#     def from_entity(user: DomainUser) -> "UserShow":
#         return UserShow(
#             first_name=user.first_name,
#             last_name=user.last_name,
#             middle_name=user.middle_name,
#             email=user.email,
#             role=user.role.name,
#             number_phone=user.number_phone,
#             time_call=user.time_call,
#             status=user.status.name
#         )


class UserUpdate(UserCreate):
    pass
