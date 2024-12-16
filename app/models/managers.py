from enum import Enum
from typing import Optional
from sqlalchemy import String, Enum as SQLAEnum
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Role(str, Enum):
    MANAGER = "Manager"
    SUPER_MANAGER = "SuperManager"
    ADMIN = "Admin"


class Manager(Base):
    __tablename__ = "manager"

    tg_id: Mapped[int] = mapped_column(primary_key=True, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(30))
    name: Mapped[Optional[str]]
    role: Mapped[Role] = mapped_column(SQLAEnum(Role), default=Role.MANAGER)
