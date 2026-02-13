import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from enchante.utils import optional

__all__ = ["EmailsUpdate", "EmailsCreate", "Emails"]


class EmailsCreate(BaseModel):
    pass


class Emails(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uid: uuid.UUID
    created_at: datetime
    updated_at: datetime | None

@optional
class EmailsUpdate(Emails):
    pass