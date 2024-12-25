from fastapi import APIRouter, Depends, status
from typing import List

from app.services.base import IManagersService
from app.schemas.managers import ManagerSchema, ManagerNameSchema
from app.dependencies import get_manager_service

router = APIRouter(
    prefix="/managers",
    tags=["managers"],
)


@router.get(
    "/",
    response_model=List[ManagerSchema],
    operation_id="readManagers",
    status_code=status.HTTP_200_OK,
)
async def read_managers(service: IManagersService = Depends(get_manager_service)):
    """
    Получить список всех менеджеров.
    """
    return await service.get_managers()


@router.get(
    "/{tg_id}",
    response_model=ManagerSchema | None,
    operation_id="getManager",
    status_code=status.HTTP_200_OK,
)
async def get_manager_by_id(
    tg_id: int, service: IManagersService = Depends(get_manager_service)
):
    """
    Получить менеджера по Telegram ID.
    """
    return await service.get_by_tg_id(tg_id=tg_id)


@router.post(
    "/",
    response_model=ManagerSchema,
    operation_id="createManager",
    status_code=status.HTTP_201_CREATED,
)
async def create_manager(
    schema: ManagerSchema, service: IManagersService = Depends(get_manager_service)
):
    """
    Создать нового менеджера.
    """
    return await service.create_manager(schema)


@router.put(
    "/{tg_id}",
    response_model=ManagerSchema,
    operation_id="changeName",
    status_code=status.HTTP_200_OK,
)
async def change_name(
    tg_id: int,
    schema: ManagerNameSchema,
    service: IManagersService = Depends(get_manager_service),
):
    """
    Изменить имя менеджера по Telegram ID.
    """
    return await service.change_name_by_tg_id(tg_id=tg_id, name=schema.name)


@router.delete(
    "/{tg_id}", operation_id="deleteManager", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_manager(
    tg_id: int, service: IManagersService = Depends(get_manager_service)
):
    await service.delete_manager(tg_id=tg_id)
