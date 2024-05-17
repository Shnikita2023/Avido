from application.events import IsApprovedAd, DomainCommand
from application.infrastructure.message_bus import subscribe
from application.services.ad.ad import advertisement_service


def filter_by_is_approve_ad(command: DomainCommand) -> bool:
    return isinstance(command, IsApprovedAd)


@subscribe(filter_by_is_approve_ad)
async def is_approve_ad(command: IsApprovedAd):
    await advertisement_service.change_ad_status_on_active_or_rejected(command.ad_oid, command.is_approved)


