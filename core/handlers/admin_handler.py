from aiogram import Router, F
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder


from core.filters.admin_filter import IsAdmin, IsSuperManager
from loader import db, dp

router = Router()

@router.message(IsSuperManager())
@router.message(F.text == '👤 Выдать/Забрать админ-права',IsAdmin())
async def give_admin_root(message: Message):
    managers = db.get_managers()
    
    kb = InlineKeyboardBuilder()
    
    if len(managers) > 1:
        for manager in managers:
            if dp.manager.id == int(manager[0]):
                continue
            kb.button(text= manager[1], callback_data=f'id_{manager[0]}')

        kb.adjust(2)

    else:
        kb.button(text='Список пуст', callback_data='no_managers')
    await message.answer('Введите пользователя:', 
                         reply_markup=kb.as_markup(resize_keyboard=True, 
                                                   one_time_keyboard=True))


@router.message(~IsSuperManager())
@router.message(F.text == '👤 Выдать/Забрать админ-права',~IsAdmin())
async def no_rights(message: Message):
    await message.answer('У вас нет прав администратора сервера!')
