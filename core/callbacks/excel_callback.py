import os
from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext

from core.states.states_form import Period
from database.excel import create_excel

router = Router()

callback_period = ['period_7', 'period_30', 'period_all']

@router.callback_query(Period.period, F.data.in_(callback_period))
async def period_callback(query: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    period = query.data.split('_')[-1]

    excel_name = create_excel(period=period)

    document = FSInputFile(path=excel_name)
    await query.message.answer_document(document=document, 
                                        caption='Все отчеты за указанный период')
    os.remove(path=excel_name)

        
