from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.config import get_session
from app.repositories.managers import ManagerRepository
from app.services.base import IManagersService, IReportsService
from app.services.managers_service import ManagersService
from app.services.reports_service import ReportsService
from app.services.calculation_service import FinancialCalculationService
from .repositories import get_manager_repository


def get_manager_service(
    repository: ManagerRepository = Depends(get_manager_repository),
) -> IManagersService:
    return ManagersService(repository)


def get_financial_service() -> FinancialCalculationService:
    return FinancialCalculationService()


def get_reports_service(
    session: AsyncSession = Depends(get_session),
    finansial_service: FinancialCalculationService = Depends(get_financial_service),
) -> IReportsService:
    return ReportsService(session, finansial_service)
