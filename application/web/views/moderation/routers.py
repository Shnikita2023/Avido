from typing import Annotated

from fastapi import APIRouter, status, Depends

from application.services.moderation import ModerationService, get_moderation_service
from application.services.user import get_user_service, UserService
from application.web.views.moderation.schemas import ModerationOutput, ModerationInput

router = APIRouter(prefix="/moderation",
                   tags=["Moderation"])


@router.get(path="/",
            summary="Получение модерации",
            status_code=status.HTTP_200_OK,
            response_model=ModerationOutput)
async def get_moderation(moderation_service: Annotated[ModerationService, Depends(get_moderation_service)],
                         moderation_oid: str) -> ModerationOutput:
    moderation = await moderation_service.get_moderation_by_id(moderation_oid)
    return ModerationOutput.to_schema(moderation)


@router.post(path="/",
             summary="Cоздание модерации",
             status_code=status.HTTP_201_CREATED,
             response_model=ModerationOutput)
async def add_moderation(moderation_service: Annotated[ModerationService, Depends(get_moderation_service)],
                         user_service: Annotated[UserService, Depends(get_user_service)],
                         moderation_schema: ModerationInput) -> ModerationOutput:
    user_service.check_user_role_allowed(role=("ADMIN", "MODERATOR"))
    moderation = await moderation_service.create_moderation(moderation_schema.to_domain())
    return ModerationOutput.to_schema(moderation)
