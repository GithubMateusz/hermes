from edgy import EdgySettings
from esmerald import EsmeraldAPISettings


class Settings(EsmeraldAPISettings):
    app_name: str = "hermes"
    title: str = "Hermes API"
    version: str = "0.0.1"
    description: str = "Hermes API"
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
    debug: bool = True

    chat_model: str = "gpt-3.5-turbo"
    embedding_model: str = "text-embedding-3-small"


class DatabaseSettings(EdgySettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/hermes"
    preloads: list[str] = ["backend.hermes.models"]


settings = Settings()
database_settings = DatabaseSettings()
