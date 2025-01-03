import asyncio
import sys

from bot.loader import create_bot_dispatcher
from bot.utils.logger import bot_logger

# Импорт всех необходимых хэндлеров
from bot.handlers import (
    basic_handler,
    report_handler,
    # Добавьте другие импорты handlers
)

# Импорт всех необходимых коллбэков
from bot.callbacks import (
    report_callback,
    # Добавьте другие импорты callbacks
)


async def main():
    """
    Основная точка входа для запуска бота
    """
    bot, dp = create_bot_dispatcher()

    # Регистрация роутеров
    dp.include_routers(
        basic_handler.router,
        report_handler.router,
        report_callback.router,
        # Добавьте другие роутеры
    )

    # Логирование старта
    bot_logger.info("Бот запускается...")

    try:
        # Удаление вебхуков и старта поллинга
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
