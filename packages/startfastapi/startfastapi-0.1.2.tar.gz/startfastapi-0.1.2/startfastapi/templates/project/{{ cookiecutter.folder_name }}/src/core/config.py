from urllib import parse
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from src.core.logger import logger


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="allow", case_sensitive=True)

    SRV_HOST: str = Field(default="0.0.0.0")
    SRV_PORT: int = Field(default=80)
    SRV_WORKERS: int = Field(default=1)
    SRV_WORKERS_THREADS: int = Field(default=1)
    SRV_WORKERS_CONNECTIONS: int = Field(default=1)
    SRV_REQUEST_TIMEOUT: int = Field(default=600)

    API_DEBUG: bool = Field(default=True)

    DB_HOST: str = Field(default="localhost")
    DB_PORT: int = Field(default=3306)
    DB_USER: str =  Field(default="root")
    DB_PASSWORD: str = Field(default="root")
    DB_DATABASE: str = Field(default="db")
    DB_ECHO: bool = Field(default=True)
    DB_CHARSET: str = Field(default="utf8mb4")
    DB_AUTO_FLUSH: bool = Field(default=True)
    DB_EXPIRE_COMMIT: bool = Field(default=False)
    DB_POOL_SIZE: int = Field(default=20)
    DB_POOL_MAX_OVERFLOW: int = Field(default=20)
    DB_POOL_TIMEOUT: int = Field(default=30)
    DB_POOL_RECYCLE: int = Field(default=3600)

    SECRET_KEY: str = Field()
    SECRET_ALGORITHM: str = Field()
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field()

    @property
    def DB_ENCODE_PASSWORD(self) -> str:
        return parse.quote_plus(self.DB_PASSWORD)

    @property
    def DB_URL_STR_ASYNC(self) -> str:
        return f"mysql+asyncmy://{self.DB_USER}:{self.DB_ENCODE_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_DATABASE}?charset={self.DB_CHARSET}"

    @property
    def DB_URL_STR_SYNC(self) -> str:
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_ENCODE_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_DATABASE}?charset={self.DB_CHARSET}"


settings = Settings()


logger.info('Settings:')
for k, v in settings.model_dump().items():
    logger.info(f'\t{k}: {v}')