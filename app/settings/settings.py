import os

from dotenv import load_dotenv
from pydantic import BaseSettings

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


class CommonSettings(BaseSettings):
    APP_NAME: str = str(os.environ.get('APP_NAME'))
    DEBUG_MODE: bool = str(os.environ.get('DEBUG_MODE'))


class ServerSettings(BaseSettings):
    APP_HOST: str = str(os.environ.get('APP_HOST'))
    APP_PORT: int = int(os.environ.get('APP_PORT'))


class DatabaseSettings(BaseSettings):
    DB_URL: str = str(os.environ.get('DB_URL'))
    DB_NAME: str = str(os.environ.get('DB_NAME'))


class Settings(CommonSettings, ServerSettings, DatabaseSettings):
    pass


settings = Settings()
