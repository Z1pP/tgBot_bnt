from aiogram import Router, F
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder


from core.filters.admin_filter import IsAdmin
from loader import db

router = Router()

@router.message(F.text == '👤 Выдать/Забрать админ-права',IsAdmin())
async def give_admin_root(message: Message):
    managers = db.get_managers()
    
    kb = InlineKeyboardBuilder()
    
    if len(managers) > 1:
        for manager in managers:
            kb.button(text= manager[2], callback_data=f'id_{manager[0]}')

        kb.adjust(2)

    else:
        kb.button(text='Список пуст', callback_data='no_managers')
    await message.answer('Введите пользователя:', 
                         reply_markup=kb.as_markup(resize_keyboard=True, 
                                                   one_time_keyboard=True))


@router.message(F.text == '👤 Выдать/Забрать админ-права',~IsAdmin())
async def no_rights(message: Message):
    await message.answer('У вас нет прав администратора сервера!')


# Админ команда для тестирования времени сна бота
@router.message(F.text == '!сон', IsAdmin())
async def show_time_until_notification(message:Message):
    import pytz
    from datetime import datetime, timedelta

    belarus_tz = pytz.timezone('Europe/Minsk')

    start_time = belarus_tz.localize(datetime.now().replace(hour=18, minute=50, second=0, microsecond=0))
    end_time = belarus_tz.localize(datetime.now().replace(hour=23, minute=30, second=0, microsecond=0))
    current_time = datetime.now(tz=belarus_tz)

    current_day = current_time.weekday()
    if current_day not in [0, 1, 2, 3, 4]:
        await message.answer('Бот спит! Сегодня выходной' )
        return
    # Проверка, чтобы бот не писал с 16:50 до 23:30
    if not start_time.time() <= current_time.time() <= end_time.time():
        time_sleep = start_time - current_time
        if time_sleep.total_seconds() > 0:
            hours, remainder = divmod(int(time_sleep.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            await message.answer(f'Бот спит! Проснется через {hours} часов, {minutes} минут, {seconds} секунд')
        else:
            # Проверка и получение времени сна для следующего дня
            next_day_start_time = start_time + timedelta(days=1)
            time_sleep = next_day_start_time - current_time
            hours, remainder = divmod(int(time_sleep.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            await message.answer(f'Бот спит! Проснется завтра через {hours} часов, {minutes} минут, {seconds} секунд')
    else:
        await message.answer('Бот не спит!')

