from typing import Optional
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext

from keyboards.reply import reply_keyboard_manager, default_keyboard
from states.states_form import Registration, ChangeName
from data.config import BASE_URL
from services.manager_api_service import ManagerApiService
from dto.manager import ManagerDTO

router = Router()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext) -> None:
    service = ManagerApiService(base_url=BASE_URL, endpoint="managers")
    tg_id = message.from_user.id
    manager: Optional[ManagerDTO] = await service.get_manager_by_id(id=tg_id)

    if manager:
        await message.answer(
            f"Привет {manager.username}, я бот для отчетов.\n"
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
async def work_menu(message: Message) -> None:
    service = ManagerApiService(base_url=BASE_URL, endpoint="managers")
    tg_id = message.from_user.id

    manager = await service.get_manager_by_id(id=tg_id)

    await message.answer(
        f"Отлично {manager["name"]}, теперь я готов к работе!",
        reply_markup=reply_keyboard_manager(manager["role"]),
    )


@router.message(F.text == "🖊 Изменить имя")
async def change_name(message: Message, state: FSMContext) -> None:
    await message.answer("Введите новое имя:")
    await state.set_state(ChangeName.name)


# Обработчик для изменения имени
@router.message(
    StateFilter(ChangeName.name), lambda x: x.text.isalpha() and (2 < len(x.text) <= 10)
)
async def change_manager_name(message: Message, state: FSMContext) -> None:
    await state.clear()

    service = ManagerApiService(base_url=BASE_URL, endpoint="managers")
    tg_id = message.from_user.id

    updated_name = message.text.strip().capitalize()
    upload_data = {"name": updated_name}

    try:
        manager = await service.update_manager_name(id=tg_id, data=upload_data)
        await message.answer(
            f"{manager["name"]}, имя успешно измененно!",
            reply_markup=default_keyboard,
        )
    except Exception as e:
        await message.answer(
            f"Произошла ошибка при попытке изменить имя! {str(e)}",
            reply_markup=default_keyboard,
        )


# Обработчик для регистрации
@router.message(
    StateFilter(Registration.name),
    lambda x: x.text.isalpha() and (2 < len(x.text) <= 10),
)
async def registration(message: Message, state: FSMContext) -> None:
    await state.clear()

    service = ManagerApiService(base_url=BASE_URL, endpoint="managers")
    tg_id = message.from_user.id

    register_name = message.text.strip().capitalize()
    upload_data = {
        "tg_id": tg_id,
        "username": message.from_user.first_name,
        "name": register_name,
    }

    manager = await service.create_manager(data=upload_data)

    if manager:
        await message.answer(
            f"Привет {manager["name"]}, я бот для отчетов.\n"
            + 'Для начала работы нажми внизу "Начать работу" ',
            reply_markup=default_keyboard,
        )
        return


# Обработчик валидации имени при вводе
@router.message(StateFilter(ChangeName.name, Registration.name))
async def not_correct_name(message: Message) -> None:
    await message.answer(
        "⛔️ Внимание! ⛔️\n Имя должно быть короче 2 символов и не длинее 10, а также не содержит "
        "цифр!\n" + "Пожалуйста, введите корректное имя:"
    )
