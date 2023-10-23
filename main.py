import asyncio
import logging
import pytz

from datetime import datetime, timedelta

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
    # Установка часового пояса для Беларуси
    belarus_tz = pytz.timezone('Europe/Minsk')

    # Временные рамки для отправления уведомления
    start_time = belarus_tz.localize(datetime.now().replace(hour=16, minute=50, second=0, microsecond=0))
    end_time = belarus_tz.localize(datetime.now().replace(hour=23, minute=30, second=0, microsecond=0))

    while True:
        current_time = datetime.now(tz=belarus_tz)
        # Проверка что не выходной день
        if current_time.weekday() not in [0, 1, 2, 3, 4]:
            time_sleep = 60*60*24 # Бот засыпает на сутки
            await asyncio.sleep(time_sleep)
            continue
        # Проверка, чтобы бот не писал с 16:50 до 23:30
        if not start_time.time() <= current_time.time() <= end_time.time():
            time_sleep = start_time - current_time
            if time_sleep.total_seconds() > 0:
                await asyncio.sleep(time_sleep.total_seconds())
            else:
                # Проверка и получение времени сна для следующего дня
                next_day_start_time = start_time + timedelta(days=1)
                time_sleep = next_day_start_time - current_time
                await asyncio.sleep(time_sleep.total_seconds())
                continue

        # Получение списка менеджеров из БД
        managers_list = db.get_managers()
        
        # Проверка что список не пустой
        if not managers_list:
            await asyncio.sleep(60*60) # Ожидание 1 час
            continue

        #Получение даты в формате строки
        current_date = datetime.now(belarus_tz).strftime('%d.%m.%Y')
        report_list = db.get_report_list_by_date(current_date)

        for manager in managers_list:
            # Проверка, что менеджер отправил отчет за текущий день
            if not any(manager[0] in report for report in report_list):
                # Отправка уведомления если отчет не отправлен
                try:
                    await bot.send_message(
                    chat_id=manager[0],
                    text=f'Напоминаю, что вам необходимо сделать отчет за {current_date}!'
                )
                except Exception as e:
                    logging.exception(e) # Логирование на случай ошибки
                    continue
        await asyncio.sleep(60*30) # Ожидание 30 минут


async def main():
    dp.include_routers(
        basic_handler.router,
        report_handler.router,
        excel_handler.router,
        admin_handler.router,
        report_callback.router,
        admin_callback.router,
        excel_callback.router
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

async def rubot():
    await asyncio.gather(main(), check_report_status())

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(rubot())