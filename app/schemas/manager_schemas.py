from typing import Optional
from pydantic import BaseModel

from app.models import Manager


class ManagerSchema(BaseModel):
    tg_id: int
    username: str
    name: Optional[str] = None
    role: Optional[str] = None

    class Config:
        from_attributes = True

    @classmethod
    def from_model(cls, model: Manager) -> "ManagerSchema":
        return cls(
            tg_id=model.tg_id, username=model.username, name=model.name, role=model.role
        )


class ManagerUpdateSchema(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
