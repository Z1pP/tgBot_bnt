from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage

from bot.data.config import BOT_TOKEN, USE_REDIS
from bot.utils.logger import bot_logger


def create_bot_dispatcher():
    """
    Создание бота и диспетчера с настройкой хранилища состояний

    :return: Кортеж (Bot, Dispatcher)
    """
    # Выбор хранилища состояний
    if USE_REDIS:
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

    # Создание бота и диспетчера
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher(storage=storage)

    bot_logger.info("Бот и диспетчер успешно инициализированы")

    return bot, dp
