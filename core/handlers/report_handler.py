from aiogram import Router, F
from aiogram.types import Message, Chat
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.states.states_form import ReportState
from core.keyboards.inline import get_keyboard
from core.keyboards.inline_date import get_keyboard_date
from core.keyboards.reply import reply_keyboard_manager
from core.filters.admin_filter import IsSuperManager
from reports.report import Report
from loader import db

router = Router()

data_for_report: dict = {}


@router.message(F.text == "📑 Сформировать отчёт")
async def start_create_report(message: Message) -> None:

    await message.answer(
        "Вы готовы начать формирвать сегодняшний отчет?",
        reply_markup=get_keyboard(key="filling_form"),
    )


async def create_report(chat: Chat, state: FSMContext) -> None:
    manager = db.get_manager_to_id(id=chat.id)
    manager_name = manager[0][2]
    await state.update_data(manager=manager_name)

    await chat.bot.send_message(
        chat_id=chat.id, text="Введите количество обработанных запросов:"
    )
    await state.set_state(ReportState.orders)


@router.message(
    StateFilter(ReportState.orders),
    lambda x: x.text.isdigit() and 0 <= int(x.text),
)
async def get_orders(message: Message, state: FSMContext) -> None:
    await state.update_data(orders=message.text)

    await message.answer("Введите количество выставленных счетов:")
    await state.set_state(ReportState.invoices)


@router.message(StateFilter(ReportState.orders))
async def orders_not_digit(message: Message) -> None:
    await message.answer(
        "⛔️ Внимание! ⛔️\n Указан неверный формат данных!\n"
        + "Возможно вы ввели отрицательное число...\n"
        + "Введите количество обработанных запросов:"
    )


@router.message(
    StateFilter(ReportState.invoices),
    lambda x: x.text.isdigit() and 0 <= int(x.text),
)
async def get_invoices(message: Message, state: FSMContext) -> None:
    await state.update_data(invoices=message.text)

    await message.answer("Введите количество оплаченных заказов:")
    await state.set_state(ReportState.paid)


@router.message(StateFilter(ReportState.invoices))
async def invoices_not_digit(message: Message) -> None:
    await message.answer(
        "⛔️ Внимание! ⛔️\n Указан неверный формат данных!\n"
        + "Возможно вы ввели отрицательное число...\n"
        + "Введите количество выставленных счетов:"
    )


@router.message(
    StateFilter(ReportState.paid), lambda x: x.text.isdigit() and 0 <= int(x.text)
)
async def get_payments(message: Message, state: FSMContext) -> None:
    await state.update_data(paid=message.text)

    await message.answer("Укажите маржу:")
    await state.set_state(ReportState.margin)


@router.message(StateFilter(ReportState.paid))
async def paid_not_digit(message: Message) -> None:
    await message.answer(
        "⛔️ Внимание! ⛔️\n Указан неверный формат данных!\n"
        + "Возможно вы ввели отрицательное число...\n"
        + "Введите количество оплаченных заказов:"
    )


@router.message(
    StateFilter(ReportState.margin),
    lambda x: ("-" not in x.text)
    and (x.text.replace(".", "", 1).isdigit() or x.text.replace(",", "", 1).isdigit()),
)
async def get_margine(message: Message, state: FSMContext) -> None:
    await state.update_data(margin=message.text.replace(",", ".", 1))

    await message.answer("Укажите полученную выручку:")
    await state.set_state(ReportState.revenue)


@router.message(StateFilter(ReportState.margin))
async def margin_not_digit_and_not_less_zero(message: Message) -> None:
    await message.answer(
        "⛔️ Внимание! ⛔️\n Указан неверный формат данных!\n"
        + "Возможно вы ввели отрицательное число...\n"
        + "Введите корректно маржу:"
    )


@router.message(
    StateFilter(ReportState.revenue),
    lambda x: ("-" not in x.text)
    and (x.text.replace(".", "", 1).isdigit() or x.text.replace(",", "", 1).isdigit()),
)
async def get_revenue(message: Message, state: FSMContext) -> None:
    await state.update_data(revenue=message.text.replace(",", ".", 1))

    await message.answer(
        "Рассчеты принимаемс с НДС равным 1.2?", reply_markup=get_keyboard(key="nds")
    )
    await state.set_state(ReportState.nds)


@router.message(StateFilter(ReportState.revenue))
async def revenue_not_digit_and_not_less_zero(message: Message) -> None:
    await message.answer(
        "⛔️ Внимание! ⛔️\n Указан неверный формат данных!\n"
        + "Возможно вы ввели отрицательное число...\n"
        + "Введите корректно полученную выручку:"
    )


@router.message(ReportState.nds, F.text)
async def get_nds(message: Message, state: FSMContext) -> None:
    await state.update_data(nds=message.text)

    await check_report_is_correct(message, state)


async def check_report_is_correct(chat: Chat, state: FSMContext) -> None:
    global data_for_report
    data_for_report = await state.get_data()

    answer_text = f"""
    Заказов обработанно - {data_for_report['orders']},
    Счетов выставленно - {data_for_report['invoices']},
    Заказов оплаченно - {data_for_report['paid']},
    Маржа - {data_for_report['margin']},
    Полученная выручка - {data_for_report['revenue']},
    НДС - {data_for_report['nds']}"""

    await chat.bot.send_message(
        chat_id=chat.id,
        text="Проверьте указанные данные:\n" + answer_text,
        reply_markup=get_keyboard(key="check_report"),
    )
    await state.clear()


async def save_report(chat: Chat) -> None:
    report = Report(**data_for_report)
    report.id = chat.id
    # Сохранение отчета в базу данных
    manager = db.get_manager_to_id(chat.id)
    db.add_report_to_db(report=report)

    text = """
    ✅ Отлично, ваш отчет успешно сохранен!
    Он добавлен в базу данных для формирования недельного отчета"""

    await chat.bot.send_message(
        chat_id=chat.id, text=text, reply_markup=reply_keyboard_manager(manager[0][0])
    )


@router.message(F.text == "📁 Полный список отчетов", IsSuperManager())
async def get_report_list(message: Message):
    # Получение всех отчетов из базы данных
    report_list = db.get_report_list()

    # Проверка наличия отчетов
    if not report_list:
        await message.answer("Список отчетов пуст!")
        return

    answer = get_report_for_answer(report_list)
    report_count = len(answer)

    for i, report in enumerate(answer):
        report_id = report_list[i][0]
        delete_kd = InlineKeyboardBuilder()
        delete_kd.button(text="🗑 Удалить", callback_data=f"delete_report_{report_id}")
        markup = delete_kd.as_markup()

        # Объединить текста отчета и кнопки
        report_text = f"Отчет {i + 1} из {report_count}:\n{report}"
        await message.answer(report_text, reply_markup=markup)


@router.message(F.text == "📅 Получить отчёты по дате", IsSuperManager())
async def get_report_by_date(message: Message):
    await message.answer("Введите дату:", reply_markup=get_keyboard_date())


async def get_report_by_date_from_db(message: Message, date: str):
    report_list = db.get_report_list_by_date(date)

    answer = get_report_for_answer(report_list)
    report_count = len(answer)

    for i, report in enumerate(answer):
        report_id = report_list[i][0]
        delete_kd = InlineKeyboardBuilder()
        delete_kd.button(text="🗑 Удалить", callback_data=f"delete_report_{report_id}")
        markup = delete_kd.as_markup()

        # Объединить текст отчета и кнопку с помощью join
        report_text = f"Отчет {i + 1} из {report_count}:\n{report}"
        await message.answer(report_text, reply_markup=markup)


def report_dict_to_string(report_dict: dict) -> str:
    # Преобразование списка данных в одну строку для отправки
    string = "\n".join(
        f"{k}: {v}%" if k == "Процент наценки" else f"{k}: {v}"
        for k, v in report_dict.items()
    )
    return string


def get_report_for_answer(report_list: list) -> list:
    answer = []
    # Формирование отчетов в одно сообщение
    for report in report_list:
        answer.append(
            report_dict_to_string(
                report_dict=report_list_to_dict(report_from_db=report)
            )
        )
    return answer


def report_list_to_dict(report_from_db: list) -> dict:
    return {
        "Дата создания": report_from_db[1],
        "Имя": report_from_db[2],
        "Заказов обработано": report_from_db[4],
        "Счетов выставлено": report_from_db[5],
        "Счетов оплачено": report_from_db[6],
        "Маржа": report_from_db[7],
        "Выручка": report_from_db[8],
        "Конверсия": report_from_db[9],
        "Конверсия счета в оплату": report_from_db[10],
        "Процент наценки": report_from_db[11],
    }
