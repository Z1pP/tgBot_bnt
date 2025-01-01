from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional

from app.models.report_models import Report
from app.schemas.report_schemas import ReportSchemaInput, ReportSchemaOutput


@dataclass
class ReportDTO:
    """
    DTO для работы с отчетами
    """

    manager_tg_id: int
    total_orders: int
    total_invoices: int
    paid_invoices: int
    total_margin: Decimal
    total_revenue: Decimal
    nds: Optional[Decimal] = Decimal("1.2")

    # Необязательные поля
    id: Optional[int] = None
    conversion_rate: Optional[Decimal] = None
    paid_conversion_rate: Optional[Decimal] = None
    markup_percentage: Optional[Decimal] = None

    # Метаданные
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def create(
        cls,
        manager_tg_id: int,
        total_orders: int,
        total_invoices: int,
        paid_invoices: int,
        total_margin: Decimal,
        total_revenue: Decimal,
        nds: Optional[Decimal] = Decimal("1.2"),
        **kwargs,
    ) -> "ReportDTO":
        """
        Создание DTO с дополнительными параметрами
        """
        return cls(
            manager_tg_id=manager_tg_id,
            total_orders=total_orders,
            total_invoices=total_invoices,
            paid_invoices=paid_invoices,
            total_margin=total_margin,
            total_revenue=total_revenue,
            nds=nds,
            **kwargs,
        )

    @classmethod
    def from_model(cls, model: Report) -> "ReportDTO":
        """
        Создание DTO из ORM модели
        """
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

    @classmethod
    def from_schema(cls, schema: ReportSchemaInput) -> "ReportDTO":
        """
        Создание DTO из входной схемы
        """
        return cls(
            manager_tg_id=schema.manager_tg_id,
            total_orders=schema.total_orders,
            total_invoices=schema.total_invoices,
            paid_invoices=schema.paid_invoices,
            total_margin=schema.total_margin,
            total_revenue=schema.total_revenue,
            nds=schema.nds or Decimal("1.2"),
        )

    def to_schema(self) -> ReportSchemaOutput:
        """
        Преобразование в выходную схему
        """
        return ReportSchemaOutput(
            id=self.id,
            manager_tg_id=self.manager_tg_id,
            total_orders=self.total_orders,
            total_invoices=self.total_invoices,
            paid_invoices=self.paid_invoices,
            total_margin=self.total_margin,
            total_revenue=self.total_revenue,
            nds=self.nds,
            conversion_rate=self.conversion_rate or Decimal("0.0"),
            paid_conversion_rate=self.paid_conversion_rate or Decimal("0.0"),
            markup_percentage=self.markup_percentage or Decimal("0.0"),
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
