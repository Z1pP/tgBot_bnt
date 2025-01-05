from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.states.states_form import Period
from bot.filters.admin_filter import IsSuperManager
from bot.keyboards.inline_date import reply_keyboard_period


router = Router()


# Обработка команды связанных с excel
@router.message(F.text == "📝 Получить отчеты в Excel файле", IsSuperManager())
async def get_report_in_excel(message: Message, state: FSMContext) -> None:
    await message.answer(
        "Выберите период за который хотите получить отчеты в Excel",
        reply_markup=reply_keyboard_period(),
    )
    await state.set_state(Period.period)
