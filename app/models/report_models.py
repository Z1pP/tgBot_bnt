from datetime import datetime
from typing import TYPE_CHECKING
from decimal import Decimal

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import func, DateTime, Integer, ForeignKey
from sqlalchemy.types import DECIMAL

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.manager_models import Manager


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    manager_tg_id: Mapped[int] = mapped_column(
        ForeignKey("managers.tg_id"), nullable=False
    )
    # Метрики прожал
    total_orders: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )  # Обработанные заказы
    total_invoices: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )  # Выставленные счета
    paid_invoices: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )  # Оплаченных счетов

    # Финансовые показатели
    total_margin: Mapped[Decimal] = mapped_column(
        DECIMAL(precision=10, scale=2), nullable=False
    )  # Маржа
    total_revenue: Mapped[Decimal] = mapped_column(
        DECIMAL(precision=10, scale=2), nullable=False
    )  # Полученная выручка от счета

    # Дополнительные вычисляемые метрики
    conversion_rate: Mapped[Decimal] = mapped_column(
        DECIMAL(precision=5, scale=2), nullable=True
    )
    paid_conversion_rate: Mapped[Decimal] = mapped_column(
        DECIMAL(precision=5, scale=2), nullable=True
    )
    markup_percentage: Mapped[Decimal] = mapped_column(
        DECIMAL(precision=5, scale=2), nullable=True
    )

    # Временные метки
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=False
    )

    # Связь с менеджером
    manager: Mapped["Manager"] = relationship(back_populates="reports", lazy="selectin")
