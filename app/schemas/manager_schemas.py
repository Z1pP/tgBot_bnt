from typing import Optional
from pydantic import BaseModel

from app.dtos.manager_dto import ManagerDTO


class ManagerSchema(BaseModel):
    tg_id: int
    username: str
    name: Optional[str] = None
    role: Optional[str] = None

    class Config:
        from_attributes = True

    @classmethod
    def from_dto(cls, dto: ManagerDTO) -> "ManagerSchema":
        return cls(tg_id=dto.tg_id, username=dto.username, name=dto.name, role=dto.role)


class ManagerUpdateSchema(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
