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

    @classmethod
    def create(cls, report_data: dict) -> "ReportEnriry":
        try:
            return cls(
                manager_tg_id=int(report_data["manager_tg_id"]),
                total_orders=int(report_data["total_orders"]),
                total_invoices=int(report_data["total_invoices"]),
                paid_invoices=int(report_data["paid_invoices"]),
                total_margin=Decimal(report_data["total_margin"]),
                total_revenue=Decimal(report_data["total_revenue"]),
                nds=Decimal(report_data["nds"]),
            )
        except (ValueError, TypeError) as e:
            raise ValueError(f"Ошибка преобразования данных: {e}")
