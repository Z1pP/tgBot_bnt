from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.manager_repository import ManagerRepository
from app.repositories.report_repository import ReportRepository
from app.database.config import get_session


def get_manager_repository(
    session: AsyncSession = Depends(get_session),
) -> ManagerRepository:
    return ManagerRepository(session)


def get_report_repository(
    session: AsyncSession = Depends(get_session),
) -> ReportRepository:
    return ReportRepository(session)
