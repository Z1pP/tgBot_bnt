from aiogram import Router, F
from aiogram.types import CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext

from core.states.states_form import ReportState
from .report_handler import save_report, create_report, get_report_by_date_from_db, check_report_is_correct

router = Router()

# Проверяет ответ пользователя после заполнения формы
@router.callback_query(F.data.startswith('confirmation_'))
async def check_report_on_correct(query: CallbackQuery, state: FSMContext) -> None:
    try:
        if 'yes' in query.data:
            await save_report(query.message)
        elif 'no' in query.data:
            markup = ReplyKeyboardMarkup(keyboard=[
                [KeyboardButton(text='Начать работу')]
            ], resize_keyboard=True)
            await query.message.answer('Заполните форму заново!', reply_markup=markup)
            await state.clear()
        await query.answer()
    except Exception as e:
        await query.answer(f"Произошла ошибка: {str(e)}")


# Проверяет ответ пользователя перед заполнением формы
@router.callback_query(F.data.startswith('filling_form_')) 
async def conf_for_form(query: CallbackQuery, state: FSMContext) -> bool:
    try:
        if 'yes' in query.data:
            await state.set_state(ReportState.manager)
            await create_report(query.message, state)
        elif 'no' in query.data:
            markup = ReplyKeyboardMarkup(keyboard=[
                [KeyboardButton(text='Начать работу')]
            ], resize_keyboard=True)
            await query.message.answer('В другой раз!', reply_markup=markup)
            await state.clear()
        await query.answer()
    except Exception as e:
        await query.answer(f"Произошла ошибка: {str(e)}")


@router.callback_query(ReportState.nds, F.data.startswith('nds_'))
async def nds_callback(query: CallbackQuery, state: FSMContext) -> None:
    try:
        if 'yes' in query.data:
            await state.update_data(nds=1.2)
            await check_report_is_correct(query.message, state)
        elif 'no' in query.data:
            await query.message.answer('Укажите НДС:')
            await state.set_state(ReportState.nds)
        await query.answer()
    except Exception as e:
        await query.answer(f"Произошла ошибка: {str(e)}")


@router.callback_query(F.data.startswith('report_date_'))
async def date_callback(query: CallbackQuery) -> None:
    try:
        date = query.data.split('_')[-1]
        await get_report_by_date_from_db(query.message, date)
        await query.answer()
    except Exception as e:
        await query.answer(f"Произошла ошибка: {str(e)}")
