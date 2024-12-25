from enum import Enum
from typing import Optional

from sqlalchemy import String, Enum as SQLAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Role(str, Enum):
    MANAGER = "Manager"
    SUPER_MANAGER = "SuperManager"
    ADMIN = "Admin"


class Manager(Base):
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
