from fastapi import APIRouter, Depends, status


from app.schemas.reports import ReportSchemaInput, ReportSchemaOutput
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
    return await service.get_reports_by_tg_id(tg_id=manager_id)


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
