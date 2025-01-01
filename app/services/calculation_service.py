from decimal import Decimal

from app.schemas.report_schemas import ReportSchemaInput, ReportSchemaOutput


class FinancialCalculationService:
    def calculate_metrics(self, report: ReportSchemaInput) -> ReportSchemaOutput:
        """
        Расчет финансовых метрик для отчета

        Args:
            report: Входная схема отчета

        Returns:
            Схема отчета с расcчитанными метриками
        """
        return ReportSchemaOutput(
            conversion_rate=self._conversion_rate(report),
            paid_conversion_rate=self._paid_conversion_rate(report),
            markup_percentage=self._markup_percentage(report),
            **report.model_dump()
        )

    def _conversion_rate(self, report: ReportSchemaInput) -> Decimal:
        """Расчет конверсии заказов в счета"""
        try:
            return Decimal(report.total_invoices * 100) / Decimal(report.total_orders)
        except ZeroDivisionError:
            return Decimal("0.0")

    def _paid_conversion_rate(self, report: ReportSchemaInput) -> Decimal:
        """Расчет конверсии счетов в оплату"""
        try:
            return Decimal(report.paid_invoices * 100) / Decimal(report.total_invoices)
        except ZeroDivisionError:
            return Decimal("0.0")

    def _markup_percentage(self, report: ReportSchemaInput) -> Decimal:
        """Расчет процента наценки"""
        try:
            return (report.total_margin * Decimal("100")) / (
                report.total_revenue / (report.nds or Decimal("1.2"))
            )
        except ZeroDivisionError:
            return Decimal("0.0")
