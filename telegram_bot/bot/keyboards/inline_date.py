from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_keyboard_date() -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()

    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def reply_keyboard_period() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="За неделю", callback_data="period_7")
    kb.button(text="За месяц", callback_data="period_30")
    kb.button(text="За все время", callback_data="period_all")

    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)
