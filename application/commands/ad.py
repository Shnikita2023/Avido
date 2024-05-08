from application.domain.moderation.moderation import Moderation
from application.infrastructure.bus.local import DomainCommand, subscribe
from application.services.ad import AdvertisementService


def filter_by_approve_ad(command: DomainCommand) -> bool:
    return isinstance(command, Moderation.ApproveAd)


@subscribe(filter_by_approve_ad)
async def approve_ad(command: DomainCommand):

    service = AdvertisementService()

    await service.approve(command.ad_id)

