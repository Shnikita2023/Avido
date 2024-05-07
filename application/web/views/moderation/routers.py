from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from application.exceptions.base import ApplicationException
from application.services.moderation import moderation_service
from application.web.views.moderation.schemas import ModerationOutput, ModerationInput

router = APIRouter(prefix="/Moderation",
                   tags=["Moderation"])


@router.get(path="/",
            summary="Получение модерации",
            status_code=status.HTTP_200_OK,
            response_model=ModerationOutput)
async def get_moderation(moderation_oid: UUID) -> ModerationOutput:
    try:
        return await moderation_service.get_moderation_by_id(moderation_oid)

    except ApplicationException as ex:
        raise HTTPException(status_code=400, detail=ex.message)


@router.post(path="/",
             summary="Cоздание модерации",
             status_code=status.HTTP_201_CREATED,
             response_model=ModerationOutput)
async def add_moderation(moderation: ModerationInput) -> ModerationOutput:
    try:
        return await moderation_service.create_moderation(moderation)

    except ApplicationException as ex:
        raise HTTPException(status_code=400, detail=ex.message)
