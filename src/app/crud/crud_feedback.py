from datetime import datetime, timezone
from pydantic import BaseModel
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.base import CRUDBase
from app.models.feedback import Feedback, FeedbackUpdate


class CRUDFeedback(CRUDBase[Feedback, FeedbackUpdate, FeedbackUpdate]):
    ...


feedback = CRUDFeedback(Feedback)
