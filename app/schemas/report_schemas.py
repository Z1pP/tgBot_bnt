from datetime import datetime
from pydantic import BaseModel
from decimal import Decimal
from typing import Optional


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
