from typing import Optional, Type, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dtos.manager_dto import ManagerDTO
from app.models import Manager


class ManagerRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, manager_dto: ManagerDTO) -> ManagerDTO:
        """
        Создание нового менеджера
        """
        # Проверка уникальности менеджера
        existing = await self.get_by_tg_id(manager_dto.tg_id, return_type=Manager)
        if existing:
            raise ValueError("Менеджер с такам tg_id уже существует")

        manager_model = Manager(
            tg_id=manager_dto.tg_id,
            username=manager_dto.username,
            name=manager_dto.name,
            role=manager_dto.role,
        )

        self._session.add(manager_model)
        await self._session.commit()
        await self._session.refresh(manager_model)

        return ManagerDTO.from_model(manager_model)

    async def get_by_tg_id(
        self, tg_id: int, *, return_type: Optional[Type] = ManagerDTO
    ) -> Optional[Union[ManagerDTO, Manager]]:
        """
        Получение менеджера по Telegram ID с гибким возвратом

        Args:
            tg_id: Telegram ID менеджера
            return_type: Тип возвращаемого объекта
                (ManagerDTO, Manager)

        Returns:
            Объект менеджера в указанном формате
        """
        result = await self._session.execute(
            select(Manager).where(Manager.tg_id == tg_id)
        )
        manager_model = result.scalar_one_or_none()

        if not manager_model:
            return None

        if return_type is ManagerDTO:
            return ManagerDTO.from_model(manager_model)
        elif return_type is Manager:
            return manager_model
        else:
            raise ValueError(f"Неподдерживаемый тип возврата - f{return_type}")

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[ManagerDTO]:
        result = await self._session.execute(select(Manager).offset(skip).limit(limit))
        managers_models = result.scalars().all()

        return [ManagerDTO.from_model(manager) for manager in managers_models]

    async def change_by_id(self, tg_id: int, *, params: dict) -> Optional[ManagerDTO]:
        """
        Изменение информации о менеджере
        """
        manager_model: Optional[Manager] = await self.get_by_tg_id(
            tg_id, return_type=Manager
        )

        if not manager_model:
            return None

        for key, value in params.items():
            if hasattr(manager_model, key):
                setattr(manager_model, key, value)
            else:
                # TODO: добавить логгирование
                print(f"Не известный аттрибут: {key}")

        try:
            await self._session.commit()
            await self._session.refresh(manager_model)

            return ManagerDTO.from_model(manager_model)
        except Exception as e:
            await self._session.rollback()
            print(f"Ошибка обновления менеджера: {str(e)}")
            return None

    async def delete(self, tg_id: int) -> None:
        manager_model: Optional[Manager] = await self.get_by_tg_id(
            tg_id, return_type=Manager
        )

        if not manager_model:
            raise ValueError("Нет менеджера с таким tg_id")

        await self._session.delete(manager_model)
        await self._session.commit()
