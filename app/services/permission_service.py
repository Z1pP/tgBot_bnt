from typing import Optional

from app.repositories.manager_repository import ManagerRepository
from app.models.manager_models import Manager, Role
from app.models.report_models import Report


class ReportPermissionMixin:
    def __init__(self, repository) -> None:
        self._repository = repository

    async def _is_admin_or_super_manager(self, manager_tg_id: int) -> bool:
        manager_repository = ManagerRepository(self._repository._session)
        manager_model: Optional[Manager] = await manager_repository.get_by_tg_id(
            manager_tg_id
        )

        return bool(
            manager_model and manager_model.role in [Role.SUPER_MANAGER, Role.ADMIN]
        )

    async def _check_report_ownership(
        self, report: Report, current_manager_tg_id: int
    ) -> bool:
        return (
            report.manager_tg_id == current_manager_tg_id
            or await self._is_admin_or_super_manager(
                manager_tg_id=current_manager_tg_id
            )
        )
