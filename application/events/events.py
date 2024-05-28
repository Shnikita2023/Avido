from dataclasses import dataclass


@dataclass
class DomainEvent:
    pass


@dataclass
class IsApprovedAd(DomainEvent):
    ad_oid: str
    is_approved: bool
