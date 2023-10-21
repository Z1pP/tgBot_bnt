from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

from loader import db
from core.keyboards.reply import reply_keyboard_manager

router = Router()


@router.callback_query(F.data.startswith('id_'))
async def id_callback(query: CallbackQuery, bot: Bot) -> None:
    await query.answer()
    manager_id = query.data.split('_')[-1]

    # Получени данных о выбранном менеджере
    manager = db.get_manager_to_id(manager_id)
    manager_name = manager[0][2]
    current_role = manager[0][3]

    # Проверяем, не пытаемся ли мы поменять роль себе
    if manager_id == str(query.message.chat.id):
        await query.message.answer(
            text='Вы не можете удалить самого себя!',
            reply_markup= reply_keyboard_manager(query.message.chat.id)
        )
        return
    try:
        new_role = db.change_manager_role(id=manager_id, current_role=current_role)
        await query.message.answer(
            text = f'Роль пользователя {manager_name} изменена на {new_role}.'
        )
        # Сообщаем менеджеру что его роль изменена
        await bot.send_message(
            chat_id = manager_id,
            text = f'Администратор изменил вашу роль на {new_role}' +
                'Для применения новых функций перезагрузите бот командой /start'
        )
    except Exception as e:
        await query.answer(text = f"Произошла ошибка: {str(e)}")


@router.callback_query(F.data.startswith('delete_manager_'))
async def delete_manager_callback(query: CallbackQuery) -> None:
    await query.answer()
    manager_id = query.data.split('_')[-1]
    # Проверяем, не пытаемся ли мы удалить себя
    if manager_id == str(query.message.chat.id):
        await query.message.answer(
            text = 'Вы не можете удалить самого себя!',
            reply_markup= reply_keyboard_manager(query.message.chat.id)
        )
        return
    # Удаление менеджера
    try:
        db.delete_manager_from_db(id=manager_id)
        await query.message.answer(text = 'Пользователь удален.')
    except Exception as e:
        await query.answer(text = f"Произошла ошибка при попытке удаления: {str(e)}")