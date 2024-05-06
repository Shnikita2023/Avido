from .database import async_session_maker
from application.services.uof.unit_of_work import SqlAlchemyUnitOfWork


def get_unit_of_work() -> SqlAlchemyUnitOfWork:
    return SqlAlchemyUnitOfWork(session_factory=async_session_maker)
