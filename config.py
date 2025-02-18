import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    DB_URL : str = os.getenv("DB_URL")
    MIGRATION_SCRIPT_PATH : str = os.getenv("MIGRATION_SCRIPT_PATH")
    WEEKLY_PLAN_CSV_FILE_NAME : str = os.getenv("WEEKLY_PLAN_CSV_FILE_NAME")
    DAILY_SCHEDULE_CSV_FILE_NAME : str = os.getenv("DAILY_SCHEDULE_CSV_FILE_NAME")
    DEFAULT_RESOURCE_PATH : str = os.getenv("DEFAULT_RESOURCE_PATH")

settings = Settings()