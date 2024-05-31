import logging

from application.domain.entities.user import User as DomainUser
from application.infrastructure.brokers.consumers.handlers import MessageHandler
from application.services.user import UserService, get_user_service

logger = logging.getLogger(__name__)

message_handler: MessageHandler = MessageHandler()


def filter_by_is_approve_user(message: dict) -> bool:
    """Любая логика по проверки событие"""
    return True


@message_handler.register_handler(message_type="UserRegisteredEvent", predicate=filter_by_is_approve_user)
async def create_user(decode_message: dict) -> None:
    user: DomainUser = DomainUser.from_json(decode_message.get("message"))
    await UserService().create_user(user)


@message_handler.register_handler(message_type="UserUpdatedStatusEvent", predicate=filter_by_is_approve_user)
async def update_status_user(decode_message: dict) -> None:
    update_user_by_status: DomainUser = DomainUser.from_json(decode_message.get("message"))
    service: UserService = get_user_service()
    user: DomainUser = await service.get_user_by_all_params({"email": update_user_by_status.email.value})
    await service.update_user(user_oid=user.oid, new_user=update_user_by_status)
    logger.info(f"Status user {user.oid} update to {update_user_by_status.status.value}")

