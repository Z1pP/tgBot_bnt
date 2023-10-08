from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from loader import db


def get_keyboard_date() -> InlineKeyboardMarkup:
    reports = db.get_reports_date()
    keyboard_builder = InlineKeyboardBuilder()

    if not reports:
        keyboard_builder.button(text='Отчетов пока нет', callback_data='no_reports')
        return keyboard_builder.as_markup()

    for report in reports:
        report_date = report[0]
        keyboard_builder.button(text=f'Отчет за {report_date}',
                                callback_data=f'report_date_{report_date}')
    
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()