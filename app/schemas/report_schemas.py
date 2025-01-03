from datetime import datetime
from pydantic import BaseModel
from decimal import Decimal
from typing import Optional

from app.dtos.report_dto import ReportDTO


class ReportSchemaInput(BaseModel):
    manager_tg_id: int
    total_orders: int
    total_invoices: int
    paid_invoices: int
    total_margin: Decimal
    total_revenue: Decimal
    nds: Decimal | None = Decimal("1.2")


class ReportSchemaOutput(ReportSchemaInput):
    id: Optional[int] = None
    conversion_rate: Decimal
    paid_conversion_rate: Decimal
    markup_percentage: Decimal
    updated_at: Optional[datetime] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

    @classmethod
    def from_dto(cls, dto: ReportDTO) -> "ReportSchemaOutput":
        return cls(
            id=dto.id,
            manager_tg_id=dto.manager_tg_id,
            total_orders=dto.total_orders,
            total_invoices=dto.total_invoices,
            paid_invoices=dto.paid_invoices,
            total_margin=dto.total_margin,
            total_revenue=dto.total_revenue,
            conversion_rate=dto.conversion_rate or Decimal("0.0"),
            paid_conversion_rate=dto.paid_conversion_rate or Decimal("0.0"),
            markup_percentage=dto.markup_percentage or Decimal("0.0"),
            created_at=dto.created_at,
            updated_at=dto.updated_at,
        )
