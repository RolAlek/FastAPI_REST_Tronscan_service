from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent.parent


class APISettings(BaseModel):
    host: str
    port: int
    debug: bool


class DatabaseSettings(BaseModel):
    driver: str
    host: str
    port: int
    user: str
    password: str
    name: str

    @property
    def url(self) -> str:
        return f"{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="allow",
        env_file=".env",
        env_nested_delimiter="_",
        case_sensitive=False,
    )

    api: APISettings
    database: DatabaseSettings


settings = Settings()
