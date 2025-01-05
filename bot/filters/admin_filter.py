from aiogram.filters import BaseFilter
from aiogram.types import Message

from core.config import setting


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in setting.ADMINS


class IsSuperManager(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return True
