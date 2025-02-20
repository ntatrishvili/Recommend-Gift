from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    database_url: str = Field(
        default="sqlite+aiosqlite:///./gifts.db",
        env="DATABASE_URL"
    )
    log_level: str = "INFO"
    gpt_model: str = "gpt-4-1106-preview"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()