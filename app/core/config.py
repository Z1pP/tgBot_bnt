import os
from dotenv import load_dotenv

load_dotenv()


class Setting:

    API_HOST = os.getenv("API_HOST") or "localhost"
    API_PORT = int(os.getenv("API_PORT") or "8000")

    DB_NAME = os.getenv("DB_NAME") or "test.db"


setting = Setting()
