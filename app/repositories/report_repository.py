from datetime import datetime
from typing import List, Optional

from sqlalchemy import select, and_, delete, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.dtos.report_dto import ReportDTO
from app.models.report_models import Report
from app.repositories.exceptions import (
    ReportNotFoundException,
    ReportAlreadyExistsException,
)


class ReportRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, report_dto: ReportDTO) -> ReportDTO:
        """
        Создание нового отчета.
        """
        report_model = Report(
            manager_tg_id=report_dto.manager_tg_id,
            total_orders=report_dto.total_orders,
            total_invoices=report_dto.total_invoices,
            paid_invoices=report_dto.paid_invoices,
            total_margin=report_dto.total_margin,
            total_revenue=report_dto.total_revenue,
            conversion_rate=report_dto.conversion_rate,
            paid_conversion_rate=report_dto.paid_conversion_rate,
            markup_percentage=report_dto.markup_percentage,
        )

        try:
            self._session.add(report_model)
            await self._session.commit()
            await self._session.refresh(report_model)
        except IntegrityError:
            raise ReportAlreadyExistsException(report_dto.id)

    async def get_by_id(self, report_id: int) -> Optional[ReportDTO]:
        """
        Получение отчета по его ИД
        """
        query = select(Report).where(Report.id == report_id)
        result = await self._session.execute(query)
        report_model = result.scalar_one_or_none()

        if not report_model:
            raise ReportNotFoundException(report_id)

        return ReportDTO.from_model(report_model)

    async def get_by_manager_id(
        self,
        manager_tg_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[ReportDTO]:
        query = select(Report).where(Report.manager_tg_id == manager_tg_id)

        if start_date:
            query = query.where(Report.created_at >= start_date)
        if end_date:
            query = query.where(Report.created_at <= end_date)

        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def update(self, report_id: int, **kwargs) -> Optional[ReportDTO]:
        """Обновляем отчет"""
        query = (
            update(Report)
            .where(Report.id == report_id)
            .values(**kwargs)
            .returning(Report)
        )
        result = await self._session.execute(query)
        report_model = result.scalar_one_or_none()

        if not report_model:
            raise ReportNotFoundException(report_id)

        return ReportDTO.from_model(report_model)

    async def delete(self, report_id: int) -> bool:
        """Удалить репорт по его ИД"""
        query = delete(Report).where(Report.id == report_id)
        result = await self._session.execute(query)
        await self._session.commit()
        return result.rowcount > 0

    async def get_latest_report(self, manager_tg_id: int) -> Optional[ReportDTO]:
        """Получить последний репорт менеджера"""
        query = (
            select(Report)
            .where(Report.manager_tg_id == manager_tg_id)
            .order_by(Report.created_at.desc())
        )
        result = await self._session.execute(query)
        return result.scalar_one_or_none()

    async def get_reports_in_period(
        self,
        manager_tg_id: int,
        start_date: datetime,
        end_date: datetime,
    ) -> List[Report]:
        query = select(Report).where(
            and_(
                Report.manager_tg_id == manager_tg_id,
                Report.created_at >= start_date,
                Report.created_at <= end_date,
            )
        )
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def get_all_reports(self) -> List[ReportDTO]:
        """Получить все репорты"""
        query = select(Report)
        result = await self._session.execute(query)
        return list(result.scalars().all())
