from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


from app.schemas.reports import ReportSchemaInput, ReportSchemaOutput
from app.models.report import Report
from app.services.base import IReportsService
from app.services.calculation_service import FinancialCalculationService


class ReportsService(IReportsService):
    def __init__(
        self, session: AsyncSession, finansial_service: FinancialCalculationService
    ):
        self.session = session
        self._finansial_service = finansial_service

    async def get_reports_by_tg_id(self, tg_id: int) -> list[ReportSchemaOutput]:
        query = select(Report).where(Report.manager_tg_id == tg_id)
        try:
            result = await self.session.execute(query)
            return result.scalars().all()
        except Exception as e:
            print(f"Ошибка при получении отчета: {str(e)}")
            return []

    async def create_report(self, report: ReportSchemaInput) -> ReportSchemaOutput:
        try:
            return self._finansial_service.calculate_metrics(report)
        except Exception as e:
            print(f"Не удалось создать отчет: {str(e)}")
            raise
