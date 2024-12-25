import asyncio
import logging

from loader import dp, bot
from handlers import (
    basic_handler,
    report_handler,
    excel_handler,
    admin_handler,
)
from callbacks import report_callback, excel_callback, admin_callback
from utils import commands
from services import check_connection

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("bot.log"), logging.StreamHandler()],
)

logger = logging.getLogger("bot")


async def initialize_bot():
    logger.info("Проверка API")
    api_alive = await check_connection()
    if api_alive is False:
        logger.error("API недоступно. Бот не будет запущен.")
        return

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

    await commands.set_commands(bot)
    logger.info("Команды бота установлены")


async def start_polling():
    try:
        logger.info("Старт пулинга")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Произошла ошибка при запуске бота: {e}")


async def close_bot_sessions():
    logger.info("Закрытие сессии бота")
    await bot.session.close()
    await dp.storage.close()


async def main():
    await initialize_bot()
    await start_polling()
    await close_bot_sessions()


if __name__ == "__main__":
    asyncio.run(main())
