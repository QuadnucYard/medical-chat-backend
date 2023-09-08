from sqlmodel import SQLModel, col, select, func, extract
from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.base import CRUDBase
from app.models.complaint import Complaint, ComplaintCreate


class CRUDComplaint(CRUDBase[Complaint, ComplaintCreate, SQLModel]):
    async def count_by_create_date(self, db: AsyncSession):
        return await self.count_by_date(db, Complaint.create_time)

    async def count_by_resolve_date(self, db: AsyncSession):
        return await self.count_by_date(db, Complaint.resolve_time)


complaint = CRUDComplaint(Complaint)
