from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from core.states.states_form import ReportState
from core.keyboards.inline import get_keyboard
from core.keyboards.inline_date import get_keyboard_date

from loader import db, dp

router = Router()

@router.message(F.text == '📑 Сформировать отчёт')
async def start_create_report(message:Message) -> None:

    await message.answer('Вы готовы начать формирвать сегодняшний отчет?', 
                         reply_markup= get_keyboard(key='filling_form'))


async def create_report(message: Message, state: FSMContext) -> None:
    await state.update_data(manager = dp.manager)
    
    await message.answer('Введите количество заказов:')
    await state.set_state(ReportState.orders)


@router.message(StateFilter(ReportState.orders),
                lambda x: x.text.isdigit() and 0 <= int(x.text) <= 50)
async def get_orders(message: Message, state: FSMContext) -> None:
    await state.update_data(orders = message.text)

    await message.answer('Введите количество обработанных заказов:')
    await state.set_state(ReportState.invoices)


@router.message(StateFilter(ReportState.orders))
async def orders_not_digit(message: Message) -> None:
    await message.answer('Написана хрень 1')


@router.message(StateFilter(ReportState.invoices),
                lambda x: x.text.isdigit() and 0 <= int(x.text) <= 50)
async def get_invoices(message: Message, state: FSMContext) -> None:
    await state.update_data(invoices = message.text)

    await message.answer('Введите количество оплаченных заказов:')
    await state.set_state(ReportState.paid)


@router.message(StateFilter(ReportState.invoices))
async def invoices_not_digit(message: Message) -> None:
    await message.answer('Написана хрень 2')


@router.message(ReportState.paid, F.text)
async def get_payments(message: Message, state: FSMContext) -> None:
    await state.update_data(paid = message.text)

    await message.answer('Укажите маржу:')
    await state.set_state(ReportState.margin)


@router.message(ReportState.margin, F.text)
async def get_margine(message: Message, state: FSMContext) -> None:
    await state.update_data(margin = message.text)

    await message.answer('Укажите полученную выручку:')
    await state.set_state(ReportState.revenue)


@router.message(ReportState.revenue, F.text)
async def get_revenue(message: Message, state: FSMContext) -> None:
    await state.update_data(revenue = message.text)

    await message.answer('Рассчеты принимаемс с НДС равным 1.2?',
                         reply_markup=get_keyboard(key='nds'))
    await state.set_state(ReportState.nds)


@router.message(ReportState.nds, F.text)
async def get_nds(message: Message, state: FSMContext) -> None:
    await state.update_data(nds = message.text)

    await check_report_is_correct(message, state)


async def check_report_is_correct(message: Message, state: FSMContext) -> None:
    global data_state
    data_state = await state.get_data()

    answer_text = f'''
    Заказов пришло - {data_state['orders']},
    Заказов обработанных - {data_state['invoices']},
    Заказов оплаченных - {data_state['paid']},
    Маржа - {data_state['margin']},
    Полученная выручка - {data_state['revenue']},
    НДС - {data_state['nds']}'''

    await message.answer('Проверьте указанные данные:\n' + answer_text,
                         reply_markup=get_keyboard(key='check_report'))
    await state.clear()


async def save_report(message: Message) -> None:
    report = dp.manager.create_report(data=data_state)

    #Сохранение отчета в базу данных
    db.add_report_to_db(report=report)

    text = 'Окей, ваш отчет успешно занесен в таблицу!'
    await message.answer(text)


@router.message(F.text == '📁 Список отчетов')
async def get_report_list(message: Message):
    #Получение всех отчетов из базы данных
    report_list = db.get_report_list()

    #Проверка наличия отчетов
    if not report_list:
        await message.answer('У вас нет отчетов!')
        return
    
    answer  = get_report_for_answer(report_list) 
    #Получение количества отчетов
    reports_count = len(report_list)

    #Отправка отчетов
    await message.answer(f'Всего отчетов: {str(reports_count)}\n' 
                         + '-' * 50 +'\n'
                         + '\n\n'.join(answer))


@router.message(F.text == '📅 Получить отчёты по дате')
async def get_report_by_date(message: Message):
    await message.answer('Введите дату:',
                         reply_markup=get_keyboard_date())


async def get_report_by_date_from_db(message: Message, date: str):
    report_list = db.get_report_list_by_date(date)
    
    answer = get_report_for_answer(report_list)

    reports_count = len(report_list)

    #Отправка отчетов
    await message.answer(f'Всего отчетов: {str(reports_count)}\n' 
                         + '-' * 50 +'\n'
                         + '\n\n'.join(answer))
    


def report_dict_to_string(report_dict: dict) -> str:
    # Преобразование списка данных в одну строку для отправки
    string = "\n".join(f"{k}: {v}%" if k == "Процент наценки" else f"{k}: {v}" for k, v in report_dict.items())
    return string



def get_report_for_answer(report_list: list) -> list:
    answer = []
    #Формирование отчетов в одно сообщение 
    for report in report_list:
        answer.append(
            report_dict_to_string(
                report_dict= dp.manager.report_list_to_dict(report_from_db=report)
                )
            )
    return answer
