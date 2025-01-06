from app.repositories.manager_repository import ManagerRepository
from app.models.manager_models import Manager, Role


class ReportPermissionMixin:
    async def _is_admin_or_super_manager(self, manager_tg_id: int) -> bool:
        manager_repository = ManagerRepository(self._repository._session)
        manager_model = await manager_repository.get_by_tg_id(
            manager_tg_id, return_type=Manager
        )

        return manager_model and manager_model.role in [Role.SUPER_MANAGER, Role.ADMIN]

    async def _check_report_ownership(
        self, report_id: int, current_manager_tg_id: int
    ) -> bool:
        report_dto = await self._repository.get_by_id(report_id)

        if not report_dto:
            raise ValueError(f"Отчет с ID {report_id} не найден")

        return (
            report_dto.manager_tg_id == current_manager_tg_id
            or await self._is_admin_or_super_manager(current_manager_tg_id)
        )
