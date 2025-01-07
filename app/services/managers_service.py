from typing import Sequence

from app.exceptions.repository import (
    EntityNotFoundException,
    EntityAlreadyExistsException,
)
from app.repositories.manager_repository import ManagerRepository
from app.schemas.manager_schemas import ManagerSchema
from app.services.base import IManagersService


class ManagersService(IManagersService):
    def __init__(self, repository: ManagerRepository):
        self._repository = repository

    async def get_managers(self) -> Sequence[ManagerSchema]:
        """Получить список всех менеджеров"""
        manager_models = await self._repository.get_all()

        return [ManagerSchema.from_model(model) for model in manager_models]

    async def get_by_tg_id(self, tg_id: int) -> ManagerSchema:
        """Получение менеджера по его телеграмм ИД"""
        manager_model = await self._repository.get_by_tg_id(tg_id)
        if not manager_model:
            raise EntityNotFoundException(entity="Manager", entity_id=tg_id)

        return ManagerSchema.from_model(manager_model)

    async def create_manager(self, schema: ManagerSchema) -> ManagerSchema:
        """Создание нового менеджера"""
        existing_model = await self._repository.get_by_tg_id(tg_id=schema.tg_id)

        if existing_model:
            raise EntityAlreadyExistsException(entity="Manager", entity_id=schema.tg_id)

        manager_model = await self._repository.create(
            data=schema.model_dump(exclude_unset=True)
        )

        return ManagerSchema.from_model(manager_model)

    async def update_by_tg_id(self, tg_id: int, updated_data: dict) -> ManagerSchema:
        """
        Универсальный метод обновления менеджера
        """
        # TODO: запилить валидацию

        manager_model = await self.get_by_tg_id(tg_id=tg_id)
        if not manager_model:
            raise EntityNotFoundException(entity="Manager", entity_id=tg_id)

        manager_model = await self._repository.update(
            manager_model, updated_data=updated_data
        )

        return ManagerSchema.from_model(manager_model)

    async def delete_manager(self, tg_id: int) -> None:
        """Удаляем менеджера"""
        manager_model = await self._repository.get_by_tg_id(tg_id=tg_id)
        if not manager_model:
            raise EntityNotFoundException(entity="Manager", entity_id=tg_id)
        await self._repository.delete(model=manager_model)
