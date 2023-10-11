from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_user_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.add(KeyboardButton(text='📑 Сформировать отчёт'))
    keyboard.add(KeyboardButton(text='🖊 Изменить имя'))
    keyboard.adjust(1)
    return keyboard.as_markup(
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder= 'Выберите действие ⬇'
        )


def get_admin_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.add(KeyboardButton(text='🖊 Изменить имя'))
    keyboard.add(KeyboardButton(text='📑 Сформировать отчёт'))
    keyboard.add(KeyboardButton(text='📁 Полный список отчетов'))
    keyboard.add(KeyboardButton(text='📅 Получить отчёты по дате'))
    keyboard.add(KeyboardButton(text='📝 Получить отчеты в Excel файле'))
    keyboard.add(KeyboardButton(text='👤 Выдать/Забрать админ-права'))
    keyboard.adjust(2)

    return keyboard.as_markup(
        resize_keyboard=True, 
        one_time_keyboard=False, 
        input_field_placeholder= 'Выберите действие ⬇'
        )



default_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text = 'Начать работу'
        )
    ]
], resize_keyboard=True, one_time_keyboard=True, input_field_placeholder= 'Выберите действие ⬇')


def reply_keyboard_manager(manager) -> ReplyKeyboardMarkup:
    # Определяем reply_markup в зависимости от роли пользователя

    if manager.role == 'Manager':
        return get_user_keyboard()
    else:
        return get_admin_keyboard()