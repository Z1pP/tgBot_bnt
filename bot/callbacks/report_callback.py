from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.loader import db
from bot.handlers.report_handler import (
    save_report,
    create_report,
    check_report_is_correct,
    get_report_by_date_from_db,
)
from bot.keyboards.reply import default_keyboard
from bot.states.states_form import ReportState
from bot.filters.admin_filter import IsSuperManager

router = Router()


# Проверяет согласие пользователя с указанными данными
@router.callback_query(F.data.startswith("confirmation_"))
async def check_report_on_correct(query: CallbackQuery, state: FSMContext) -> None:
    await query.answer()
    try:
        if "yes" in query.data:
            await save_report(chat=query.message.chat)
        elif "no" in query.data:
            await query.message.answer(
                text="Заполните форму заново!", reply_markup=default_keyboard
            )
            await state.clear()
    except Exception as e:
        await query.answer(text=f"Произошла ошибка: {str(e)}")


# Проверяет ответ пользователя перед заполнением формы
@router.callback_query(F.data.startswith("filling_form_"))
async def conf_for_form(query: CallbackQuery, state: FSMContext) -> None:
    await query.answer()
    try:
        if "yes" in query.data:
            await state.set_state(ReportState.manager)
            await create_report(chat=query.message.chat, state=state)
        elif "no" in query.data:
            await query.message.answer(
                text="Заполенение формы отмененно!", reply_markup=default_keyboard
            )
            await state.clear()
    except Exception as e:
        await query.answer(text=f"Произошла ошибка: {str(e)}")


# Проверяет ответ пользователя - оставить ндс или указать новый
@router.callback_query(ReportState.nds, F.data.startswith("nds_"))
async def nds_callback(query: CallbackQuery, state: FSMContext) -> None:
    await query.answer()
    try:
        if "yes" in query.data:
            await state.update_data(nds=1.2)  # Значение по умолчанию
            await check_report_is_correct(chat=query.message.chat, state=state)
        elif "no" in query.data:
            await query.message.answer(text="Укажите НДС:")
            await state.set_state(ReportState.nds)
    except Exception as e:
        await query.answer(text=f"Произошла ошибка: {str(e)}")


# Проверяет выбранную дату для формирования отчета по этой дате
@router.callback_query(IsSuperManager(), F.data.startswith("report_date_"))
async def date_callback(query: CallbackQuery) -> None:
    await query.answer()
    try:
        date = query.data.split("_")[-1]
        await get_report_by_date_from_db(message=query.message, date=date)
    except Exception as e:
        await query.answer(text=f"Произошла ошибка: {str(e)}")


@router.callback_query(IsSuperManager(), F.data.startswith("delete_report_"))
async def delete_report(query: CallbackQuery) -> None:
    await query.answer()
    try:
        report_id = int(query.data.split("_")[-1])
        db.delete_report_from_db(id=report_id)
        await query.message.answer(text="Отчет успешно удален!")
    except Exception as e:
        await query.answer(text=f"Произошла ошибка при удалении: {str(e)}")
