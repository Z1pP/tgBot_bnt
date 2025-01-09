from datetime import datetime
from pydantic import BaseModel
from decimal import Decimal
from typing import Optional

from app.models.report_models import Report


class ReportSchemaInput(BaseModel):
    manager_tg_id: int
    total_orders: int
    total_invoices: int
    paid_invoices: int
    total_margin: Decimal
    total_revenue: Decimal
    nds: Optional[Decimal] = Decimal("1.2")


class ReportSchemaUpdate(BaseModel):
    manager_tg_id: int
    total_orders: Optional[int] = None
    total_invoices: Optional[int] = None
    paid_invoices: Optional[int] = None
    total_margin: Optional[Decimal] = None
    total_revenue: Optional[Decimal] = None
    nds: Optional[Decimal] = None


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
    def from_model(cls, model: Report) -> "ReportSchemaOutput":
        return cls(
            id=model.id,
            manager_tg_id=model.manager_tg_id,
            total_orders=model.total_orders,
            total_invoices=model.total_invoices,
            paid_invoices=model.paid_invoices,
            total_margin=model.total_margin,
            total_revenue=model.total_revenue,
            nds=Decimal("1.2"),  # Значение по умолчанию
            conversion_rate=model.conversion_rate,
            paid_conversion_rate=model.paid_conversion_rate,
            markup_percentage=model.markup_percentage,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
