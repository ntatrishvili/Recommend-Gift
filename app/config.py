from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str
    database_url: str = "sqlite:///./gifts.db"
    
    class Config:
        env_file = ".env"

settings = Settings()