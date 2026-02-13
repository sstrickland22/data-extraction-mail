import uuid
from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from enchante.utils import Base


class Emails(Base):
    __tablename__ = "emailss"

    uid: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, server_default="gen_random_uuid()"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.current_timestamp
    )
    updated_at: Mapped[datetime | None]