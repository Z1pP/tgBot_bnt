from aiogram.filters import BaseFilter
from aiogram.types import Message

from core.data.config import ADMINS
from loader import db, dp

class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in ADMINS
    

class IsSuperManager(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        manager = db.get_manager_to_id(message.from_user.id)
        return manager[0][3] == dp.manager.role