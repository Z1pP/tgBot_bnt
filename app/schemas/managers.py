from typing import Optional
from pydantic import BaseModel


class ManagerSchema(BaseModel):
    tg_id: int
    username: str
    name: Optional[str] = None
    role: Optional[str] = None

    class Config:
        from_attributes = True


class ManagerNameSchema(BaseModel):
    name: str
