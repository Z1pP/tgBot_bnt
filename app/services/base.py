from abc import ABC, abstractmethod
from typing import Sequence, Optional

from app.models.manager_models import Role
from app.schemas.manager_schemas import ManagerSchema
from app.schemas.report_schemas import ReportSchemaInput, ReportSchemaOutput


class IManagersService(ABC):
    @abstractmethod
    async def get_managers(self) -> Sequence[ManagerSchema]:
        pass

    @abstractmethod
    async def get_by_tg_id(self, tg_id: int) -> Optional[ManagerSchema]:
        pass

    @abstractmethod
    async def create_manager(self, schema: ManagerSchema) -> Optional[ManagerSchema]:
        pass

    @abstractmethod
    async def update_by_tg_id(
        self, tg_id: int, updated_data: dict
    ) -> Optional[ManagerSchema]:
        pass

    @abstractmethod
    async def delete_manager(self, tg_id: int) -> None:
        pass


class IReportsService(ABC):
    @abstractmethod
    async def get_reports_by_manager(
        self, manager_tg_id: int
    ) -> list[ReportSchemaOutput]:
        pass

    @abstractmethod
    async def create_report(self, report: ReportSchemaInput) -> ReportSchemaOutput:
        pass
