from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from core.keyboards.reply import default_keyboard
from core.states.states_form import ReportState
from .report_handler import save_report, create_report, get_report_by_date_from_db, check_report_is_correct
from loader import db


router = Router()


# Проверяет ответ пользователя после заполнения формы
@router.callback_query(F.data.startswith('confirmation_'))
async def check_report_on_correct(query: CallbackQuery, state: FSMContext) -> None:
    try:
        if 'yes' in query.data:
            await save_report(query.message)
        elif 'no' in query.data:
            await query.message.answer('Заполните форму заново!', 
                                       reply_markup=default_keyboard)
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
            await query.message.answer('Заполенение формы отмененно!',
                                        reply_markup=default_keyboard)
            await state.clear()
        await query.answer()
    except Exception as e:
        await query.answer(f"Произошла ошибка: {str(e)}")


# Проверяет ответ пользователя - оставить ндс или указать новый
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


# Проверяет выбранную дату для формирования отчета по этой дате
@router.callback_query(F.data.startswith('report_date_'))
async def date_callback(query: CallbackQuery) -> None:
    try:
        date = query.data.split('_')[-1]
        await get_report_by_date_from_db(query.message, date)
        await query.answer()
    except Exception as e:
        await query.answer(f"Произошла ошибка: {str(e)}")


@router.callback_query(F.data.startswith('id_'))
async def id_callback(query: CallbackQuery) -> None:
    manager_id = query.data.split('_')[-1]
    # Получени данных о выбранном менеджере
    manager = db.get_manager_to_id(manager_id)
    manager_name = manager[0][2]
    current_role = manager[0][3]
    try:
        new_role = db.change_manager_role(id = manager_id, current_role=current_role)
        await query.message.answer(f'Роль пользователя {manager_name} изменена на {new_role}.' +
                                   'Пользователю необходимо перезапустить бот командой /start')
    except Exception as e:
        await query.answer(f"Произошла ошибка: {str(e)}")

