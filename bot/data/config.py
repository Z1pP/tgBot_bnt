import os
import enum
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Токен бота
BOT_TOKEN = os.getenv("TOKEN", "")

# Администраторы бота
ADMINS = [int(admin_id) for admin_id in os.getenv("ADMINS", "").split(",") if admin_id]

# Использовать ли Redis для хранения состояний
USE_REDIS = os.getenv("USE_REDIS", "False").lower() == "true"

BASE_URL = r"http://0.0.0.0:8000/api/v1"


# Пути и директории
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(BASE_DIR, "folder_to_reports")

# Создаем директорию для отчетов, если она не существует
os.makedirs(REPORTS_DIR, exist_ok=True)

# Настройки логирования
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Дополнительные настройки
MAX_MESSAGE_LENGTH = 4096  # Максимальная длина сообщения в Telegram
CACHE_TIME = 60  # Время кэширования inline-кнопок
