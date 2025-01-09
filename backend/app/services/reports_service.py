import logging

from app.exceptions.permission import NoPermissionException
from app.exceptions.repository import EntityNotFoundException

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
        super().__init__(repository)

    async def get_reports_by_manager(
        self, manager_tg_id: int
    ) -> list[ReportSchemaOutput]:
        report_models = await self._repository.get_by_manager_id(
            manager_tg_id=manager_tg_id
        )

        return [ReportSchemaOutput.from_model(model) for model in report_models]

    async def create_report(self, schema: ReportSchemaInput) -> ReportSchemaOutput:
        report_data = self._finansial_service.calculate_metrics(report=schema)
        report_model = await self._repository.create(
            data=report_data.model_dump(exclude_unset=True, exclude="nds")
        )
        return ReportSchemaOutput.from_model(report_model)

    async def update_report(
        self, report_id: int, schema: ReportSchemaUpdate
    ) -> ReportSchemaOutput:
        existing_report = await self._repository.get_by_id(report_id=report_id)

        if not existing_report:
            raise EntityNotFoundException(entity="Report", entity_id=report_id)

        if not await self._check_report_ownership(
            report=existing_report, current_manager_tg_id=schema.manager_tg_id
        ):
            raise NoPermissionException(
                operation="Update_report",
                details=f"Manager {schema.manager_tg_id} does not have rights fot update report",
            )

        report_model = await self._repository.update(
            model=existing_report, updated_data=schema.model_dump(exclude_unset=True)
        )

        return ReportSchemaOutput.from_model(report_model)

    async def delete_report(self, report_id: int, manager_tg_id: int) -> None:
        existing_report = await self._repository.get_by_id(report_id=report_id)

        if not existing_report:
            raise EntityNotFoundException(entity="Report", entity_id=report_id)

        if not await self._check_report_ownership(
            report=existing_report, current_manager_tg_id=manager_tg_id
        ):
            raise NoPermissionException(
                operation="Update_report",
                details=f"Manager {manager_tg_id} does not have rights for delete report",
            )

        await self._repository.delete(model=existing_report)
