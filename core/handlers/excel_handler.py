from aiogram import Router, F, Bot
from aiogram.types import Message, FSInputFile

from core.filters.admin_filter import IsSuperManager
from database.excel import create_excel


router = Router()

@router.message(F.text == '📝 Получить отчеты в Excel файле', IsSuperManager())
async def get_report_in_excel(message: Message, bot: Bot):
    file = create_excel(filename='excel.xlsx')
    document = FSInputFile(path=file,)
    await bot.send_document(message.chat.id, document=document, caption='Все отчеты')
