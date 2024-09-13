from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = 'poker api'

    db_host: str
    db_user: str
    db_port: int
    db_pass: str
    db_name: str

    model_config = SettingsConfigDict(env_file=".env")