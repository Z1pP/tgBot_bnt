from enum import Enum
from typing import Optional, TYPE_CHECKING

from sqlalchemy import String, Enum as SQLAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import DateFeild

if TYPE_CHECKING:
    from app.models.report_models import Report


class Role(str, Enum):
    MANAGER = "Manager"
    SUPER_MANAGER = "SuperManager"
    ADMIN = "Admin"


class Manager(DateFeild):
    __tablename__ = "managers"

    tg_id: Mapped[int] = mapped_column(primary_key=True, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(30))
    name: Mapped[Optional[str]]
    role: Mapped[Role] = mapped_column(SQLAEnum(Role), default=Role.MANAGER)

    reports: Mapped[list["Report"]] = relationship(
        back_populates="manager",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
