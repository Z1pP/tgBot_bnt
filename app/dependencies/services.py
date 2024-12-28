from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.config import get_session
from app.services.base import IManagersService, IReportsService
from app.services.managers_service import ManagersService
from app.services.reports_service import ReportsService
from app.services.calculation_service import FinancialCalculationService


def get_manager_service(
    session: AsyncSession = Depends(get_session),
) -> IManagersService:
    return ManagersService(session)


def get_financial_service() -> FinancialCalculationService:
    return FinancialCalculationService()


def get_reports_service(
    session: AsyncSession = Depends(get_session),
    finansial_service: FinancialCalculationService = Depends(get_financial_service),
) -> IReportsService:
    return ReportsService(session, finansial_service)
