from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.config import get_session
from app.services.base import IManagersService
from app.services.managers_service import ManagersService


def get_manager_service(
    session: AsyncSession = Depends(get_session),
) -> IManagersService:
    return ManagersService(session)
