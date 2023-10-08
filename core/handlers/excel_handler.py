from aiogram import Router, F, Bot
from aiogram.types import Message, FSInputFile

from database.excel import create_excel


router = Router()

@router.message(F.text == '📝 Получить отчеты в Excel файле')
async def get_report_in_excel(message: Message, bot: Bot):
    file = create_excel(filename='excel.xlsx')
    document = FSInputFile(path=file,)
    await bot.send_document(message.chat.id, document=document, caption='Отчеты')
