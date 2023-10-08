from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


# Формирование клавиатуры для выбора
user_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text= '📑 Сформировать отчёт'
        )
    ]
], resize_keyboard=True, one_time_keyboard=False, input_field_placeholder= 'Выберите действие ⬇')



admin_keyboard  = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text= '📑 Сформировать отчёт'
        ),
        KeyboardButton(
            text= '📁 Список отчетов'
        ),
        KeyboardButton(
            text = '📅 Получить отчёты по дате'
        ),
        KeyboardButton(
            text = '📝 Получить отчеты в Excel файле'
        )
    ]
], resize_keyboard=True, one_time_keyboard=False, input_field_placeholder= 'Выберите действие ⬇')

default_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text = 'Начать работу'
        )
    ]
], resize_keyboard=True, one_time_keyboard=False, input_field_placeholder= 'Выберите действие ⬇')

def reply_keyboard_manager(manager) -> ReplyKeyboardMarkup:
    # Определяем reply_markup в зависимости от роли пользователя

    if manager.role == 'Бомж':
        return user_keyboard
    else:
        return admin_keyboard