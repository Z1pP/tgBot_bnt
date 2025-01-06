import logging

from app.repositories.report_repository import ReportRepository
from app.schemas.report_schemas import (
    ReportSchemaInput,
    ReportSchemaOutput,
    ReportSchemaUpdate,
)
from app.services.base import IReportsService
from app.services.calculation_service import FinancialCalculationService
from app.services.permission_service import ReportPermissionMixin


logger = logging.getLogger(__name__)


class ReportsService(IReportsService, ReportPermissionMixin):
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

    async def update_report(
        self, report_id: int, report: ReportSchemaUpdate
    ) -> ReportSchemaOutput:
        try:
            if not await self._check_report_ownership(report_id, report.manager_tg_id):
                raise ValueError("Не досаточно прав чтобы изменить отчет")

            report_data = report.model_dump(exclude_unset=True)
            report_dto = await self._repository.update(
                report_id=report_id, **report_data
            )

            return ReportSchemaOutput.from_dto(report_dto)
        except Exception as e:
            logger.error(f"Ошибка при обновлении отчета: {str(e)}")
            raise

    async def delete_report(self, report_id: int, manager_tg_id: int) -> None:
        try:
            if not await self._check_report_ownership(report_id, manager_tg_id):
                raise ValueError("Не досаточно прав чтобы удалить отчет")

            is_deleted = await self._repository.delete(report_id)
            if not is_deleted:
                logger.warning("Не удалось удалить отчет")
                raise ValueError(f"Отчет с ID {report_id} не удален!")

        except Exception as e:
            logger.error(f"Ошибка при удалении отчета: {str(e)}")
            raise
