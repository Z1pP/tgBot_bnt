from datetime import datetime
from typing import List, Optional

from sqlalchemy import select, and_, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.report_models import Report


class ReportRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, report: Report) -> Report:
        """Create a new report."""
        self._session.add(report)
        await self._session.flush()
        await self._session.commit()
        return report

    async def get_by_id(self, report_id: int) -> Optional[Report]:
        """Get a report by its ID."""
        query = select(Report).where(Report.id == report_id)
        result = await self._session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_manager_id(
        self,
        manager_tg_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[Report]:
        """Get all reports for a specific manager with optional date range."""
        query = select(Report).where(Report.manager_tg_id == manager_tg_id)

        if start_date:
            query = query.where(Report.created_at >= start_date)
        if end_date:
            query = query.where(Report.created_at <= end_date)

        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def update(self, report_id: int, **kwargs) -> Optional[Report]:
        """Update a report by its ID with the provided fields."""
        query = (
            update(Report)
            .where(Report.id == report_id)
            .values(**kwargs)
            .returning(Report)
        )
        result = await self._session.execute(query)
        return result.scalar_one_or_none()

    async def delete(self, report_id: int) -> bool:
        """Delete a report by its ID."""
        query = delete(Report).where(Report.id == report_id)
        result = await self._session.execute(query)
        return result.rowcount > 0

    async def get_latest_report(self, manager_tg_id: int) -> Optional[Report]:
        """Get the latest report for a manager."""
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
        """Get all reports for a manager within a specific date range."""
        query = select(Report).where(
            and_(
                Report.manager_tg_id == manager_tg_id,
                Report.created_at >= start_date,
                Report.created_at <= end_date,
            )
        )
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def get_all_reports(self) -> List[Report]:
        """Get all reports."""
        query = select(Report)
        result = await self._session.execute(query)
        return list(result.scalars().all())
