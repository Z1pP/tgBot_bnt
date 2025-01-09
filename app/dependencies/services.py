from fastapi import Depends

from app.repositories.manager_repository import ManagerRepository
from app.repositories.report_repository import ReportRepository
from app.services.base import IManagersService, IReportsService
from app.services.managers_service import ManagersService
from app.services.reports_service import ReportsService
from app.services.calculation_service import FinancialCalculationService
from .repositories import get_manager_repository, get_report_repository


def get_manager_service(
    repository: ManagerRepository = Depends(get_manager_repository),
) -> IManagersService:
    return ManagersService(repository)


def get_financial_service() -> FinancialCalculationService:
    return FinancialCalculationService()


def get_reports_service(
    repository: ReportRepository = Depends(get_report_repository),
    finansial_service: FinancialCalculationService = Depends(get_financial_service),
) -> IReportsService:
    return ReportsService(repository, finansial_service)
