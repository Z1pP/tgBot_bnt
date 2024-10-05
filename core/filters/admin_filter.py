from aiogram.filters import BaseFilter
from aiogram.types import Message

from core.data.config import ADMINS
from loader import db


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in ADMINS


class IsSuperManager(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        manager = db.get_manager_to_id(message.from_user.id)
        role = manager[0][3]
        return role == "SuperManager"
