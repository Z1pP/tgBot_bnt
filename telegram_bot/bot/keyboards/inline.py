from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from enums import KeyboardKeys


"""Кнопки подтверждения создания отчета"""
creater_report_kb = [
    InlineKeyboardButton(text="Подтвердить", callback_data="confirmation_yes"),
    InlineKeyboardButton(text="Отменить", callback_data="confirmation_no"),
]


"""Кнопки для подтверждения начала создания отчета"""
filling_from_kb = [
    InlineKeyboardButton(text="Начать", callback_data="filling_form_yes"),
    InlineKeyboardButton(text="Отмена", callback_data="filling_form_no"),
]

check_nds_kb = [
    InlineKeyboardButton(text="Да", callback_data="nds_yes"),
    InlineKeyboardButton(text="Нет", callback_data="nds_no"),
]

keyboard = {
    KeyboardKeys.CHECK_REPORT: creater_report_kb,
    KeyboardKeys.FILING_FORM: filling_from_kb,
    KeyboardKeys.CHEKC_NDS: check_nds_kb,
}


def get_keyboard(key: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[keyboard[key]])
