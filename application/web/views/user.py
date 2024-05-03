from uuid import UUID

from fastapi import APIRouter, HTTPException

from application.services.user import UserService
from ..schemas.user import UserCreate, UserShow, UserOutput
from application.infrastructure.unit_of_work_manager import UOWDep
from application.exceptions.base import ApplicationException

router = APIRouter(prefix="/user",
                   tags=["User"])


@router.get(path="/", summary="Получение пользователя", response_model=UserShow)
async def get_user(user_oid: UUID,
                   uow: UOWDep) -> UserOutput:
    try:
        return await UserService().get_user_by_id(user_oid=user_oid, uow=uow)

    except ApplicationException as ex:
        raise HTTPException(status_code=400, detail=ex.message)


@router.post(path="/", summary="Cоздание пользователя")
async def add_user(user: UserCreate,
                   uow: UOWDep) -> UserOutput:
    try:
        return await UserService.create_user(data=user, uow=uow)

    except ApplicationException as ex:
        raise HTTPException(status_code=400, detail=ex.message)


@router.post(path="/search", summary="Поиск пользователей")
async def search_users(user_oids: list[UUID],
                       uow: UOWDep) -> list[UserOutput]:
    try:
        return await UserService().get_multi_users_by_id(user_oids)

    except ApplicationException as ex:
        raise HTTPException(status_code=400, detail=ex.message)


@router.delete(path="/", summary="Удаление пользователя")
async def delete_user(user_oid: UUID,
                      uow: UOWDep):
    try:
        return await UserService.delete_user_by_id(user_oid, uow=uow)

    except ApplicationException as ex:
        raise HTTPException(status_code=400, detail=ex.message)
