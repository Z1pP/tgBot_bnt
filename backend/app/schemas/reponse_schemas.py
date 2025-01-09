from typing import Optional, Generic, TypeVar
from pydantic import BaseModel, Field


DataT = TypeVar("DataT")


class APIResponse(BaseModel, Generic[DataT]):
    status: str = Field(default="success")
    message: Optional[str] = None
    data: Optional[DataT] = None
    total_count: Optional[int] = None

    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "message": "Operation completed successfully",
                "data": None,
                "total_count": 0,
            }
        }
