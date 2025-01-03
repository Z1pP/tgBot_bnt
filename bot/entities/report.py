from dataclasses import dataclass
from decimal import Decimal


@dataclass
class ReportEnriry:
    manager_tg_id: int
    total_orders: int
    total_invoices: int
    paid_invoices: int
    total_margin: Decimal
    total_revenue: Decimal
    nds: Decimal
