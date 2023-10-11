from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


'''Кнопки подтверждения создания отчета'''
keyboard_to_creater_report  = [
    InlineKeyboardButton(text= 'Подтвердить', callback_data='confirmation_yes'),
    InlineKeyboardButton(text= 'Отменить', callback_data='confirmation_no')
]


"""Кнопки для подтверждения начала создания отчета"""
keyboard_for_filling_from = [
    InlineKeyboardButton(text= 'Начать' ,callback_data='filling_form_yes'),
    InlineKeyboardButton(text= 'Отмена', callback_data= 'filling_form_no')
]

keyboard_for_nds = [
    InlineKeyboardButton(text= 'Да', callback_data='nds_yes'),
    InlineKeyboardButton(text= 'Нет', callback_data='nds_no')
]

keyboard = {
    'check_report': keyboard_to_creater_report,
    'filling_form': keyboard_for_filling_from,
    'nds': keyboard_for_nds
}


def get_keyboard(key: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[keyboard[key]])

