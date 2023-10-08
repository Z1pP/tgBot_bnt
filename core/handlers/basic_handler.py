import random
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart


from loader import db, dp
from core.data.config import bot_version
from core.keyboards.reply import reply_keyboard_manager, default_keyboard
from entities.managers import Manager, SuperManager

router = Router()


@router.startup()
async def database_initialization():
    print('Database initialized')
    print('Bot is running!')

# Создаем экземпляры классов Manager и DataBase
@router.message(CommandStart())
async def start(message: Message) -> None:
    user = message.from_user.first_name

    await message.answer(f'Привет {user}, я бот для отчетов.\n' +
                         f'Версия бота: {bot_version}',
                         reply_markup= default_keyboard)


@router.message(F.text == 'Начать работу')
async def work_menu(message: Message) -> None:
    name = message.from_user.first_name
    tg_id = message.from_user.id
    
    
    user = db.get_manager_to_id(id=tg_id)

    if not user:
        #Если такого нет, создается новый и кидается в бд
        manager = Manager(name=name, id=tg_id)
        db.add_managers_to_db(manager=manager)
    else:
        if user[0][2] == 'Manager':
            manager = Manager(name=name, id=tg_id)
        else:
            manager = SuperManager(name=name, id=tg_id)


    dp.manager = manager
    #Клавиатура зависит от роли
    await message.answer(f'Отлично {manager.name}, теперь я готов к работе!',
                         reply_markup=reply_keyboard_manager(manager))
    

@router.message(F.text == '/number' )
async def get_random_number(message:Message) -> None:
    number = random.randint(0,101)
    await message.reply(str(number))
