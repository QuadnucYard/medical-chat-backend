from datetime import date, datetime, timedelta
from typing import Any

from sqlalchemy import DATE
from sqlmodel import cast

time_now = datetime.now


def yesterday():
    return date.today() - timedelta(days=1)


def is_today(field: Any):
    return cast(field, DATE) == date.today()


def is_yesterday(field: Any):
    return cast(field, DATE) == yesterday()
