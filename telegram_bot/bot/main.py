import asyncio
import sys

from loader import create_bot_dispatcher
from utils.logger import bot_logger
from handlers import basic_handler, report_handler
from callbacks import report_callback


async def main():
    """
    Основная точка входа для запуска бота
    """
    bot, dp = create_bot_dispatcher()

    dp.include_routers(
        basic_handler.router,
        report_handler.router,
        report_callback.router,
    )

    bot_logger.info("Бот запускается...")

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        bot_logger.error(f"Ошибка при запуске бота: {e}", exc_info=True)
        sys.exit(1)
    finally:
        await dp.storage.close()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        bot_logger.info("Бот остановлен пользователем")
    except Exception as e:
        bot_logger.error(f"Критическая ошибка: {e}", exc_info=True)
