from pydantic import Field
from pydantic_settings import BaseSettings

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

class Settings(BaseSettings):
    database_url: str = Field(alias="DATABASE_URL")
    secret_key: str = Field(alias="SECRET_KEY")
    algorithm: str = Field(default="HS256", alias="ALGORITHM")
    access_token_expire_minutes: int = 30
    
    # Добавьте эти поля, если они нужны
    db_user: str = Field(alias="DB_USER")
    db_password: str = Field(alias="DB_PASSWORD") 
    db_name: str = Field(alias="DB_NAME")
    db_port: str = Field(default="5432", alias="DB_PORT")
    db_host: str = Field(default="localhost", alias="DB_HOST")
    
    class Config:
        env_file = ".env"

settings = Settings()