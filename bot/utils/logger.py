import logging
from logging.handlers import RotatingFileHandler
import os

os.makedirs("logs", exist_ok=True)


def setup_logger(name="bot_logger", log_file="logs/bot.log", level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = RotatingFileHandler(
        log_file, maxBytes=10 * 1024 * 1024, backupCount=5  # 10 МБ
    )

    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Другие логгеры
    aiogram_logger = logging.getLogger("aiogram")
    aiogram_logger.setLevel(logging.INFO)
    aiogram_logger.addHandler(file_handler)
    aiogram_logger.addHandler(console_handler)

    aiohttp_logger = logging.getLogger("aiohttp")
    aiohttp_logger.setLevel(logging.INFO)
    aiohttp_logger.addHandler(file_handler)
    aiohttp_logger.addHandler(console_handler)

    return logger


bot_logger = setup_logger()
