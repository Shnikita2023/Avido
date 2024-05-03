from typing import Annotated, Type

from fastapi import Depends

from .database import async_session_maker
from application.services.uof.unit_of_work import SqlAlchemyUnitOfWork


async def get_unit_of_work() -> SqlAlchemyUnitOfWork:
    return SqlAlchemyUnitOfWork(session_factory=async_session_maker)


UOWDep: Type[SqlAlchemyUnitOfWork] = Annotated[SqlAlchemyUnitOfWork, Depends(get_unit_of_work)]
