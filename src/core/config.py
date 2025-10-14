from pathlib import Path
from typing import Literal

from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict, BaseSettings


ROOT_DIR = Path(__file__).resolve().parent.parent.parent

class DBConfig(BaseModel):
    host: str
    port: int
    user: str
    db_name: str
    password: str
    
    @property
    def get_db_url(self):
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"
    

class TokenConfig(BaseModel):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ROOT_DIR/".env",
        env_nested_delimiter="__",
        env_file_encoding='utf-8',
        env_ignore_empty=True,
        extra="ignore"
    )
    mode: Literal["TEST", "LOCAL", "PROD",]
    db: DBConfig
    token: TokenConfig
    
    
settings = Settings()
