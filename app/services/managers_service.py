from typing import Optional, Sequence

from app.dtos.manager_dto import ManagerDTO
from app.repositories.manager_repository import ManagerRepository
from app.schemas.manager_schemas import ManagerSchema
from app.services.base import IManagersService


class ManagersService(IManagersService):
    def __init__(self, repository: ManagerRepository):
        self._repository = repository

    async def get_managers(self) -> Sequence[ManagerSchema]:
        """
        Получить список всех менеджеров
        """
        managers_dtos = await self._repository.get_all()
        return [ManagerSchema.from_dto(dto) for dto in managers_dtos]

    async def get_by_tg_id(self, tg_id: int) -> Optional[ManagerSchema]:
        """
        Получение менеджера по его телеграмм ИД
        """
        manager_dto = await self._repository.get_by_tg_id(tg_id)

        if manager_dto:
            return ManagerSchema.from_dto(manager_dto)
        return None

    async def create_manager(self, schema: ManagerSchema) -> Optional[ManagerSchema]:
        """
        Создание нового менеджера
        """
        created_manager_dto = await self._repository.create(
            ManagerDTO.create(**schema.model_dump(exclude_unset=True))
        )

        return ManagerSchema.from_dto(created_manager_dto)

    async def update_by_tg_id(
        self, tg_id: int, updated_data: dict
    ) -> Optional[ManagerSchema]:
        """
        Универсальный метод обновления менеджера
        """
        updated_manager = await self._repository.change_by_id(
            tg_id, params=updated_data
        )

        return ManagerSchema.from_dto(updated_manager) if updated_manager else None

    async def delete_manager(self, tg_id: int) -> None:
        """
        Удаляем менеджера
        """
        await self._repository.delete(tg_id)
