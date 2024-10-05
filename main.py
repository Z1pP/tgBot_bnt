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


async def main():
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
    # Установка команд для бота
    await commands.set_commands(bot)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        await dp.storage.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
