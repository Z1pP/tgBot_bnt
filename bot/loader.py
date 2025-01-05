from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage

from core.config import setting
from utils.logger import bot_logger


def create_bot_dispatcher():
    if setting.USE_REDIS:
        try:
            storage = RedisStorage.from_url("redis://localhost:6379/0")
            bot_logger.info("Используется Redis для хранения состояний")
        except Exception as e:
            bot_logger.warning(
                f"Не удалось подключиться к Redis: {e}. Используется MemoryStorage"
            )
            storage = MemoryStorage()
    else:
        storage = MemoryStorage()

    bot = Bot(token=setting.BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher(storage=storage)

    bot_logger.info("Бот и диспетчер успешно инициализированы")

    return bot, dp
