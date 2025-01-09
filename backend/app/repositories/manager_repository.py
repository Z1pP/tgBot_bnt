from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Manager
from app.exceptions.database import DatabaseOperationException


class ManagerRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, data: dict) -> Manager:
        """Создание нового менеджера"""
        try:
            manager_mode = Manager(**data)

            self._session.add(manager_mode)
            await self._session.commit()
            await self._session.refresh(manager_mode)
            return manager_mode

        except Exception as e:
            await self._session.rollback()
            raise DatabaseOperationException(
                operation="Create",
                entity=Manager.__name__,
                details=f"Failed to create manager: {str(e)}",
            )

    async def get_by_tg_id(self, tg_id: int) -> Optional[Manager]:
        """Получение менеджера по его Tg ID из БД"""
        try:
            result = await self._session.execute(
                select(Manager).where(Manager.tg_id == tg_id)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            raise DatabaseOperationException(
                operation="Get_by_id",
                entity=Manager.__name__,
                details=f"Failed to getting manager by his ID: {str(e)}",
            )

    async def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[Manager]:
        """Получение списка менеджеров с пагинацией"""
        try:
            result = await self._session.execute(
                select(Manager).offset(skip).limit(limit)
            )
            return result.scalars().all()
        except Exception as e:
            raise DatabaseOperationException(
                operation="Get_all",
                entity=Manager.__name__,
                details=f"Failed to getting managers: {str(e)}",
            )

    async def update(self, model: Manager, *, updated_data: dict) -> Manager:
        """
        Изменение данных менеджера
        """
        try:
            for key, value in updated_data.items():
                if hasattr(model, key):
                    setattr(model, key, value)

            await self._session.commit()
            await self._session.refresh(model)

            return model
        except Exception as e:
            await self._session.rollback()
            raise DatabaseOperationException(
                operation="Update",
                entity=Manager.__name__,
                details=f"Failed to update manager (ID: {model.tg_id}): {str(e)}",
            )

    async def delete(self, model: Manager) -> None:
        try:
            await self._session.delete(model)
            await self._session.commit()
        except Exception as e:
            await self._session.rollback()
            raise DatabaseOperationException(
                operation="Delete",
                entity=Manager.__name__,
                details=f"Failed to delete manager (ID: {model.tg_id}): {str(e)}",
            )
