from datetime import datetime
from typing import Sequence, Optional

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.report_models import Report
from app.exceptions.database import DatabaseOperationException


class ReportRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, data: dict) -> Report:
        """
        Создание нового отчета.
        """
        try:
            report_model = Report(**data)

            self._session.add(report_model)
            await self._session.commit()
            await self._session.refresh(report_model)

            return report_model
        except Exception as e:
            raise DatabaseOperationException(
                operation="Create",
                entity=Report.__name__,
                details=f"Failed to create report: {str(e)}",
            )

    async def get_by_id(self, report_id: int) -> Optional[Report]:
        """
        Получение отчета по его ИД
        """
        try:
            result = await self._session.execute(
                select(Report).where(Report.id == report_id)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            raise DatabaseOperationException(
                operation="Get_by_id",
                entity=Report.__name__,
                details=f"Failed to getting report by his ID: {str(e)}",
            )

    async def get_by_manager_id(
        self,
        manager_tg_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Sequence[Report]:
        """Получаем список отчетов для менеджера в период даты"""
        query = select(Report).where(Report.manager_tg_id == manager_tg_id)

        if start_date:
            query = query.where(Report.created_at >= start_date)
        if end_date:
            query = query.where(Report.created_at <= end_date)

        try:
            result = await self._session.execute(query)
            return result.scalars().all()
        except Exception as e:
            raise DatabaseOperationException(
                operation="Get_by_manager_id",
                entity=Report.__name__,
                details=f"Failed to getting report by manager ID: {str(e)}",
            )

    async def update(self, model: Report, updated_data: dict) -> Report:
        """Обновляем отчет"""
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
                entity=Report.__name__,
                details=f"Failed to update report (ID: {model.id}): {str(e)}",
            )

    async def delete(self, model: Report) -> None:
        """Удаление отчета"""
        try:
            await self._session.delete(model)
            await self._session.commit()
        except Exception as e:
            await self._session.rollback()
            raise DatabaseOperationException(
                operation="Delete",
                entity=Report.__name__,
                details=f"Failed to delete report (ID: {model.id}): {str(e)}",
            )

    async def get_latest_report(self, manager_tg_id: int) -> Optional[Report]:
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
    ) -> Sequence[Report]:
        query = select(Report).where(
            and_(
                Report.manager_tg_id == manager_tg_id,
                Report.created_at >= start_date,
                Report.created_at <= end_date,
            )
        )
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def get_all_reports(self) -> Sequence[Report]:
        """Получить все репорты"""
        query = select(Report)
        result = await self._session.execute(query)
        return result.scalars().all()
