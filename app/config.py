from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    amazon_access_key: str
    amazon_secret_key: str
    amazon_associate_tag: str
    amazon_region: str = "us-east-1"
    amazon_host: str = "webservices.amazon.com"
    openai_api_key: str
    database_url: str = "sqlite+aiosqlite:///./gifts.db"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
