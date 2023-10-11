import random
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext

from loader import db, dp
from core.keyboards.reply import reply_keyboard_manager, default_keyboard
from entities.managers import Manager, SuperManager
from core.states.states_form import Registration

router = Router()


@router.startup()
async def database_initialization():
    print('Database initialized')
    print('Bot is running!')


# Создаем экземпляры классов Manager и SuperManager
@router.message(CommandStart())
async def start(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    user = db.get_manager_to_id(id=user_id)
    if user:
        await message.answer(f'Привет {user[0][2]}, я бот для отчетов.\n' +
                             'Для начала работы нажми внизу "Начать работу" ',
                             reply_markup=default_keyboard)
    else:
        await message.answer('Привет новый пользователь,я бот для отчетов.\n' +
                             'Для продолжения работы необходимо ввести свое имя:')
        await state.set_state(Registration.name)


@router.message(F.text == 'Начать работу')
async def work_menu(message: Message) -> None:
    tg_name = message.from_user.first_name
    tg_id = str(message.from_user.id)

    user = db.get_manager_to_id(id=tg_id)

    if not user:
        manager = Manager(name=register_name, nickname=tg_name, id=tg_id)
        db.add_managers_to_db(manager=manager)
    else:
        manager_role = user[0][3]
        name = user[0][2]

        if manager_role == 'Manager':
            manager = Manager(name=name, nickname=tg_name, id=tg_id)
        else:
            manager = SuperManager(name=name, nickname=tg_name, id=tg_id)

    dp.manager = manager
    await message.answer(f'Отлично {manager.name}, теперь я готов к работе!',
                         reply_markup=reply_keyboard_manager(manager))


@router.message(F.text == '🖊 Изменить имя')
async def change_name(message: Message, state: FSMContext) -> None:
    await message.answer(f'Введите новое имя:')
    await state.set_state(Registration.name)


@router.message(F.text == '/number')
async def get_random_number(message: Message) -> None:
    number = random.randint(0, 101)
    await message.reply(str(number))


# Регистрируем имя нового пользователя
@router.message(StateFilter(Registration.name),
                lambda x: x.text.isalpha() and (2 < len(x.text) <= 10))
async def registration(message: Message, state: FSMContext) -> None:
    global register_name
    register_name = message.text.strip().capitalize()

    manager = db.get_manager_to_id(id=message.from_user.id)
    manager_id = manager[0][0]
    if manager:
        db.change_manager_name(new_name=register_name, id=manager_id)

    await state.clear()
    await message.answer(f'Привет {register_name}, я бот для отчетов.\n' +
                         'Для начала работы нажми внизу "Начать работу" ',
                         reply_markup=default_keyboard)


@router.message(StateFilter(Registration.name))
async def not_correct_name(message: Message) -> None:
    await message.answer('⛔️ Внимание! ⛔️\n Имя должно быть короче 2 символов и не длинее 10, а также не содержит '
                         'цифр!\n' + 'Пожалуйста, введите корректное имя:')
