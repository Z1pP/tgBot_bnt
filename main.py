import asyncio
import logging
from datetime import datetime

from loader import db, dp, bot
from core.handlers import (
    basic_handler,
    report_handler,
    excel_handler,
    admin_handler,
)
from core.callbacks import report_callback, excel_callback, admin_callback
from core.utils import commands


async def check_report_status() -> None:
    start_time = datetime.now().replace(hour=18, minute=0, second=0, microsecond=0)
    end_time = datetime.now().replace(hour=23, minute=0, second=0, microsecond=0)

    while True:
        # Проверка чтобы бот не писал с 18.00 до 2300
        if not start_time <= datetime.now() <= end_time:
            await asyncio.sleep(3600)
            continue

        current_date = datetime.now().strftime('%d.%m.%Y')
        # Получение списка менеджеров и списка отчетов за текущий день
        managers = db.get_managers()
        report_list = db.get_report_list_by_date(current_date)

        # Две проверки на наличие менеджеров и отчетов
        if not managers:
            await asyncio.sleep(3600)
            continue
        if not report_list:
            for manager in managers:
                await bot.send_message(
                    chat_id=manager[0],
                    text=f'Напоминаю, что вам необходимо сделать отчет за {current_date}!'
                )
            await asyncio.sleep(3600)
            continue
        
        # Проверка что менеджер отправил отчет за текущий день
        try:
            for manager in managers:
                for report in report_list:
                    if manager[0] not in report:
                        await bot.send_message(
                            chat_id=manager[0],
                            text=f'Напоминаю, что вам необходимо сделать отчет за {current_date}!'
                        )
        except Exception as e:
            logging.error(f'Error: {str(e)}')

        await asyncio.sleep(3600)  # Ожидание перед следующей итерацией


async def main():
    dp.include_routers(
        basic_handler.router,
        report_handler.router,
        excel_handler.router,
        admin_handler.router,
        report_callback.router,
        admin_callback.router,
    )

    # Установка соединения с БД или создание новой
    db.create_tables_or_get_exists()
    await commands.set_commands(bot)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        await dp.storage.close()

async def rubot():
    await asyncio.gather(main(), check_report_status())

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(rubot())