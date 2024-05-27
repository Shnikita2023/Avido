import json
import logging

from application.domain.entities.user import User as DomainUser
from application.infrastructure.brokers.consumers.handlers import MessageHandler
from application.services.user import UserService

logger = logging.getLogger(__name__)

message_handler: MessageHandler = MessageHandler()


@message_handler.register_handler("user_registration")
async def create_user(decode_message: str) -> None:
    user_message: dict = json.loads(decode_message)
    user: DomainUser = DomainUser.from_json(user_message.get("message"))
    await UserService().create_user(user)
