import os
from dotenv import load_dotenv

load_dotenv()


class Settings:

    # Токен бота
    BOT_TOKEN = os.getenv("TOKEN", "")

    # Администраторы бота
    ADMINS = [
        int(admin_id) for admin_id in os.getenv("ADMINS", "").split(",") if admin_id
    ]

    # Использовать ли Redis для хранения состояний
    USE_REDIS = os.getenv("USE_REDIS", "False").lower() == "true"

    API_HOST = os.getenv("API_HOST") or "localhost"
    API_PORT = int(os.getenv("API_PORT") or "8000")

    API_URL = rf"http://{API_HOST}:{API_PORT}/api/v1"


setting = Settings()
