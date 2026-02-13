from sqlalchemy.ext.asyncio import AsyncSession

from enchante.utils import CRUD
from .model import Emails
from .schema import EmailsCreate


class CRUDEmails(CRUD[Emails, EmailsCreate]):
    def __init__(self):
        super().__init__(Emails)

    async def create_new(self, db: AsyncSession, model: EmailsCreate) -> Emails:
        return await super().create_new(db, model=model)


crud = CRUDEmails()