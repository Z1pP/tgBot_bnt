from fastapi import APIRouter, Depends, status
from typing import List

from app.services.base import IManagersService
from app.schemas import APIResponse
from app.schemas.manager_schemas import ManagerSchema, ManagerUpdateSchema
from app.dependencies import get_manager_service

router = APIRouter(
    prefix="/managers",
    tags=["managers"],
)


@router.get(
    "/",
    response_model=APIResponse[List[ManagerSchema]],
    operation_id="readManagers",
    status_code=status.HTTP_200_OK,
)
async def read_managers(service: IManagersService = Depends(get_manager_service)):
    """
    Получить список всех менеджеров.
    """
    managers = await service.get_managers()
    return APIResponse(data=managers, total_count=len(managers))


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
    operation_id="changeData",
    status_code=status.HTTP_200_OK,
)
async def change_maanger_data(
    tg_id: int,
    schema: ManagerUpdateSchema,
    service: IManagersService = Depends(get_manager_service),
):
    """
    Изменить данные.
    """
    return await service.update_by_tg_id(
        tg_id=tg_id, updated_data=schema.model_dump(exclude_unset=True)
    )


@router.delete(
    "/{tg_id}", operation_id="deleteManager", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_manager(
    tg_id: int, service: IManagersService = Depends(get_manager_service)
):
    await service.delete_manager(tg_id=tg_id)
