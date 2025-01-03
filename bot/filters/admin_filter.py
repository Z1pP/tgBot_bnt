from aiogram.filters import BaseFilter
from aiogram.types import Message

from data.config import ADMINS


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in ADMINS


class IsSuperManager(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return True
