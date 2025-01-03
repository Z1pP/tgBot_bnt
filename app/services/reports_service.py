from app.schemas.report_schemas import ReportSchemaInput, ReportSchemaOutput
from app.models.report_models import Report
from app.services.base import IReportsService
from app.services.calculation_service import FinancialCalculationService
from app.repositories.report_repository import ReportRepository


class ReportsService(IReportsService):
    def __init__(
        self,
        repository: ReportRepository,
        finansial_service: FinancialCalculationService,
    ):
        self._repository = repository
        self._finansial_service = finansial_service

    async def get_reports_by_manager(
        self, manager_tg_id: int
    ) -> list[ReportSchemaOutput]:
        report_dtos = await self._repository.get_by_manager_id(manager_tg_id)

        return [ReportSchemaOutput.from_dto(dto) for dto in report_dtos]

    async def create_report(self, report: ReportSchemaInput) -> ReportSchemaOutput:
        try:
            report_data = self._finansial_service.calculate_metrics(report)
            report_dto = await self._repository.create(report_data)

            return ReportSchemaOutput.from_dto(report_dto)
        except Exception as e:
            print(f"Не удалось создать отчет: {str(e)}")
            raise
