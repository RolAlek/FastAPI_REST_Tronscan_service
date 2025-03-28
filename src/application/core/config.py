from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent.parent


class APISettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="api__")
    host: str
    port: int
    debug: bool


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="database__")
    driver: str
    host: str
    port: int
    user: str
    password: str
    name: str

    @property
    def url(self) -> str:
        return f"{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class TronAPISettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="tron__")

    api_key: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="allow",
        env_file=".env",
        env_nested_delimiter="__",
        case_sensitive=False,
    )

    api: APISettings
    database: DatabaseSettings
    tron: TronAPISettings


settings = Settings()
