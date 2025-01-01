from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.manager_repository import ManagerRepository
from app.database.config import get_session


def get_manager_repository(
    session: AsyncSession = Depends(get_session),
) -> ManagerRepository:
    return ManagerRepository(session)
