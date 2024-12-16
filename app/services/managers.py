from typing import Optional, Sequence
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.managers import ManagerSchema
from app.models.managers import Manager


class ManagersService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_managers(self) -> Sequence[ManagerSchema]:
        """
        Get all managers from db
        """
        query = select(Manager)
        result = await self.session.execute(query)
        managers = result.scalars().all()
        return [
            ManagerSchema(
                tg_id=manager.tg_id,
                username=manager.username,
                name=manager.name,
                role=manager.role,
            )
            for manager in managers
        ]

    async def get_by_tg_id(self, tg_id: int) -> Optional[ManagerSchema]:
        query = select(Manager).where(Manager.tg_id == tg_id)
        result = await self.session.execute(query)
        manager = result.scalar_one_or_none()

        if manager:
            return ManagerSchema(
                tg_id=manager.tg_id,
                username=manager.username,
                name=manager.name,
                role=manager.role,
            )
        return None

    async def create_manager(self, schema: ManagerSchema) -> Optional[ManagerSchema]:
        manager = Manager(**schema.model_dump(exclude_unset=True))
        self.session.add(manager)
        await self.session.commit()
        await self.session.refresh(manager)
        return ManagerSchema(
            tg_id=manager.tg_id,
            username=manager.username,
            name=manager.name,
            role=manager.role,
        )

    async def change_name_by_tg_id(
        self, tg_id: int, name: str
    ) -> Optional[ManagerSchema]:
        query = select(Manager).where(Manager.tg_id == tg_id)
        result = await self.session.execute(query)
        manager = result.scalar_one_or_none()

        if manager:
            manager.name = name
            await self.session.commit()
            await self.session.refresh(manager)
            return ManagerSchema(
                tg_id=manager.tg_id,
                username=manager.username,
                name=manager.name,
                role=manager.role,
            )
        return None

    async def delete_manager(self, tg_id: int) -> bool:
        query = delete(Manager).where(Manager.tg_id == tg_id)
        result = await self.session.execute(query)
        await self.session.commit()
        return result.rowcount > 0
