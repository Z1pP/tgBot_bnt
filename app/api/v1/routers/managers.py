from fastapi import APIRouter, Depends, status

from app.services.managers import ManagersService
from app.schemas.managers import ManagerSchema, ManagerNameSchema
from app.database.config import get_session

router = APIRouter(
    prefix="/managers",
    tags=["managers"],
)


def get_manager_service(session=Depends(get_session)) -> ManagersService:
    return ManagersService(session)


@router.get("/", response_model=list[ManagerSchema], operation_id="readManagers")
async def read_managers(service: ManagersService = Depends(get_manager_service)):
    return await service.get_managers()


@router.get("/{tg_id}", response_model=ManagerSchema | None, operation_id="getManager")
async def get_manager_by_id(
    tg_id: int, service: ManagersService = Depends(get_manager_service)
):
    return await service.get_by_tg_id(tg_id=tg_id)


@router.post("/", response_model=ManagerSchema, operation_id="createManager")
async def create_manager(
    schema: ManagerSchema, service: ManagersService = Depends(get_manager_service)
):
    return await service.create_manager(schema)


@router.put("/{tg_id}", response_model=ManagerSchema, operation_id="changeName")
async def change_name(
    tg_id: int,
    schema: ManagerNameSchema,
    service: ManagersService = Depends(get_manager_service),
):
    return await service.change_name_by_tg_id(tg_id=tg_id, name=schema.name)


@router.delete(
    "/{tg_id}", operation_id="deleteManager", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_manager(
    tg_id: int, service: ManagersService = Depends(get_manager_service)
):
    await service.delete_manager(tg_id=tg_id)
