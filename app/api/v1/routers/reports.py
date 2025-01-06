from fastapi import APIRouter, Depends, status

from app.schemas.report_schemas import (
    ReportSchemaInput,
    ReportSchemaOutput,
    ReportSchemaUpdate,
)
from app.dependencies.services import get_reports_service
from app.services.base import IReportsService

router = APIRouter(
    prefix="/reports",
    tags=["reports"],
)


@router.get(
    "/{manager_id}",
    response_model=list[ReportSchemaOutput],
    operation_id="GetListReportsByManagerId",
    status_code=status.HTTP_200_OK,
)
async def get_reports(
    manager_id: int,
    service: IReportsService = Depends(get_reports_service),
):
    return await service.get_reports_by_manager(manager_id)


@router.post(
    "/",
    response_model=ReportSchemaOutput,
    operation_id="CreateReport",
    status_code=status.HTTP_201_CREATED,
)
async def create_report(
    report: ReportSchemaInput,
    service: IReportsService = Depends(get_reports_service),
):
    return await service.create_report(report)


@router.put(
    "/{report_id}",
    response_model=ReportSchemaOutput,
    operation_id="UpdateReport",
    status_code=status.HTTP_200_OK,
)
async def update_report(
    report_id: int,
    report: ReportSchemaUpdate,
    service: IReportsService = Depends(get_reports_service),
):
    return await service.update_report(report_id, report)


@router.delete(
    "/{report_id}",
    response_model=None,
    operation_id="DeleteReport",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_report(
    report_id: int,
    manager_tg_id: int,
    service: IReportsService = Depends(get_reports_service),
):
    await service.delete_report(report_id, manager_tg_id)
