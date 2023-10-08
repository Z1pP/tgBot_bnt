from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from database.sqlite import DataBase

from core.data import config

bot = Bot(token= config.bot_token)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
db = DataBase('test.db')