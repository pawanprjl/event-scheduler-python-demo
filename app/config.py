from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    # Basic Settings
    APP_ENV: Literal["local", "staging", "production"] = "local"
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    # Supabase Settings
    SUPABASE_URL: str = "your url"
    SUPABASE_KEY: str = ""


# Create an instance of Settings to load environment variables
settings = Settings()
