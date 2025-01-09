import pytz
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime

moscow_tz = pytz.timezone("Europe/Moscow")


class Base(DeclarativeBase):
    pass


class DateFeild(Base):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(moscow_tz), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        insert_default=datetime.now(moscow_tz),
        onupdate=datetime.now(moscow_tz),
        nullable=False,
    )
