import asyncio
import logging

from loader import db, dp, bot
from core.handlers import (
    basic_handler,
    report_handler,
    excel_handler,
    admin_handler,
)
from core.callbacks import report_callback, excel_callback, admin_callback
from core.utils import commands

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("bot.log"), logging.StreamHandler()],
)

logger = logging.getLogger("bot")


async def main():
    logger.info("Запуск бота")

    dp.include_routers(
        basic_handler.router,
        report_handler.router,
        excel_handler.router,
        admin_handler.router,
        report_callback.router,
        admin_callback.router,
        excel_callback.router,
    )

    # Установка соединения с БД или создание новой
    db.create_tables_or_get_exists()
    logger.info("База данных инициализорванна")
    # Установка команд для бота
    await commands.set_commands(bot)
    logger.info("Команды бота установлены")
    try:
        logger.info("Старт пулинга")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Произошла ошибка при запуске бота: {e}")
    finally:
        logger.info("Закрытие сессии бота")
        await bot.session.close()
        await dp.storage.close()


if __name__ == "__main__":
    asyncio.run(main())
