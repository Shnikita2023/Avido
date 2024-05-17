from abc import ABC
from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Field as f


class BaseEntity(ABC, BaseModel):
    oid: str = f(title="Идентификатор", default_factory=lambda: str(uuid4()))
    created_at: datetime = f(title="Дата создание", default_factory=datetime.now)


