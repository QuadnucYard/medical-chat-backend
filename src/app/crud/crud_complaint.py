from sqlmodel import SQLModel

from app.crud.base import CRUDBase
from app.models.complaint import Complaint, ComplaintCreate


class CRUDComplaint(CRUDBase[Complaint, ComplaintCreate, SQLModel]):
    ...


complaint = CRUDComplaint(Complaint)
