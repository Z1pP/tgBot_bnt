import random
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext

from loader import db
from core.keyboards.reply import reply_keyboard_manager, default_keyboard
from core.states.states_form import Registration
from core.data.config import ADMINS

router = Router()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext) -> None:
    tg_id = message.from_user.id
    manager = db.get_manager_to_id(id=tg_id)

    if manager:
        await message.answer(
            f"Привет {manager[0][2]}, я бот для отчетов.\n"
            + 'Для начала работы нажми внизу "Начать работу" ',
            reply_markup=default_keyboard,
        )
    else:
        await message.answer(
            "Привет новый пользователь,я бот для отчетов.\n"
            + "Для продолжения работы необходимо ввести свое имя:",
            reply_markup=ReplyKeyboardRemove(),
        )
        await state.set_state(Registration.name)


@router.message(F.text == "Начать работу")
async def work_menu(message: Message, state: FSMContext) -> None:
    manager = db.get_manager_to_id(id=message.from_user.id)
    manager_name = manager[0][2]

    await message.answer(
        f"Отлично {manager_name}, теперь я готов к работе!",
        reply_markup=reply_keyboard_manager(manager[0][0]),
    )


@router.message(F.text == "🖊 Изменить имя")
async def change_name(message: Message, state: FSMContext) -> None:
    await message.answer("Введите новое имя:")
    await state.set_state(Registration.name)


# Регистрируем имя нового пользователя
@router.message(
    StateFilter(Registration.name),
    lambda x: x.text.isalpha() and (2 < len(x.text) <= 10),
)
async def registration(message: Message, state: FSMContext) -> None:
    await state.clear()
    tg_id = message.from_user.id

    register_name = message.text.strip().capitalize()
    manager = db.get_manager_to_id(id=tg_id)

    if not manager:
        db.add_managers_to_db(
            id=message.from_user.id,
            name=register_name,
            tg_name=message.from_user.first_name,
            role="SuperManager" if tg_id in ADMINS else "Manager",
        )
        await message.answer(
            f"Привет {register_name}, я бот для отчетов.\n"
            + 'Для начала работы нажми внизу "Начать работу" ',
            reply_markup=default_keyboard,
        )
        return

    last_name = manager[0][2]
    manager_id = manager[0][0]
    try:
        db.change_manager_name(new_name=register_name, id=manager_id)
        await message.answer(
            f"Успешно изменено имя {last_name} на {register_name}",
            reply_markup=default_keyboard,
        )
    except Exception as e:
        await message.answer(
            f"Произошла ошибка при попытке изменить имя! {str(e)}",
            reply_markup=default_keyboard,
        )


@router.message(StateFilter(Registration.name))
async def not_correct_name(message: Message) -> None:
    await message.answer(
        "⛔️ Внимание! ⛔️\n Имя должно быть короче 2 символов и не длинее 10, а также не содержит "
        "цифр!\n" + "Пожалуйста, введите корректное имя:"
    )
