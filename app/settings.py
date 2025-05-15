# app/settings.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_USER:     str
    DB_PASSWORD: str
    DB_SERVER:   str
    DB_PORT:     int
    DB_NAME:     str
    DRIVER:      str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
