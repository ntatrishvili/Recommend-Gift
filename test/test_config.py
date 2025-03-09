import os
import pytest
from app.config import Settings

def test_settings_from_env(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test_openai_api_key")
    monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///./test_gifts.db")

    settings = Settings()

    assert settings.openai_api_key == "test_openai_api_key"
    assert settings.database_url == "sqlite+aiosqlite:///./test_gifts.db"

def test_settings_default_database_url(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test_openai_api_key")

    settings = Settings()

    assert settings.openai_api_key == "test_openai_api_key"
    assert settings.database_url == "sqlite+aiosqlite:///./gifts.db"

def test_settings_from_env_file(tmpdir, monkeypatch):
    env_file = tmpdir.join(".env")
    env_file.write("OPENAI_API_KEY=test_openai_api_key_from_env_file\nDATABASE_URL=sqlite+aiosqlite:///./env_file_gifts.db")

    monkeypatch.setenv("ENV_FILE", str(env_file))

    settings = Settings(_env_file=str(env_file))

    assert settings.openai_api_key == "test_openai_api_key_from_env_file"
    assert settings.database_url == "sqlite+aiosqlite:///./env_file_gifts.db"
