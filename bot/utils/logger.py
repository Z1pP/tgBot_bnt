import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logger(name: str = "bot_logger", log_file: str = "bot.log") -> logging.Logger:
    """
    Настройка логгера с выводом в файл и консоль

    :param name: Имя логгера
    :param log_file: Путь к файлу логов
    :return: Сконфигурированный логгер
    """
    # Создаем директорию для логов, если она не существует
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Полный путь к файлу лога
    full_log_path = log_dir / log_file

    # Создаем логгер
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Форматтер для логов
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Обработчик для файла с ротацией
    file_handler = RotatingFileHandler(
        full_log_path, maxBytes=10 * 1024 * 1024, backupCount=5  # 10 МБ
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Обработчик для консоли
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Очищаем существующие обработчики
    logger.handlers.clear()

    # Добавляем обработчики
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# Создаем глобальный логгер
bot_logger = setup_logger()


# Функции-обертки для удобного логирования
def log_info(message: str):
    bot_logger.info(message)


def log_error(message: str, exc_info: bool = False):
    bot_logger.error(message, exc_info=exc_info)


def log_warning(message: str):
    bot_logger.warning(message)
