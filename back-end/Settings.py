import os
from functools import lru_cache
from pydantic_settings import BaseSettings
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import quote_plus
from typing import ClassVar

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings): 
    # App
    APP_NAME:  str = os.environ.get("APP_NAME", "Test")
    APP_URL : str = os.environ.get("APP_URL", "http://localhost:3000") 
    DEBUG: bool = bool(os.environ.get("DEBUG", False))
    
    # FrontEnd Application
    FRONTEND_HOST: str = os.environ.get("FRONTEND_HOST", "http://localhost:3000")

    # MySql Database Config
    # DATABASE_URL: str = os.getenv("DATABASE_URL", "localhost")
    # DATABASE_NAME: str = os.getenv("DATABASE_NAME", "kconnect-rms")
    # DATABASE_USER: str = os.getenv("DATABASE_USER", "root")
    # DATABASE_PASSSWORD: str = os.getenv("DATABASE_PASSSWORD", "")
    # DATABASE_URI: ClassVar[str] = f"mysql://{DATABASE_USER}:{DATABASE_PASSSWORD}@{DATABASE_URL}/{DATABASE_NAME}"

    # PostgreSQL Database Config
    #DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:@localhost/cap_table")
    #DATABASE_NAME: str = os.getenv("DATABASE_NAME", "cap_table")
    #DATABASE_USER: str = os.getenv("DATABASE_USER", "postgres")
    #DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "")
    #DATABASE_URI: ClassVar[str] = f"postgresql://{DATABASE_USER}:{quote_plus(DATABASE_PASSWORD)}@{DATABASE_URL}/{DATABASE_NAME}"
    # SQLAlchemy engine URI
    #SQLALCHEMY_DATABASE_URI: ClassVar[str] = f"postgresql://{DATABASE_USER}:{quote_plus(DATABASE_PASSWORD)}@{DATABASE_URL}/{DATABASE_NAME}"

    
    # JWT Secret Key
    JWT_SECRET: str = os.environ.get("JWT_SECRET", "649fb93ef34e4fdf4187709c84d643dd61ce730d91856418fdcf563f895ea40f")
    JWT_ALGORITHM: str = os.environ.get("ACCESS_TOKEN_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
    REFRESH_TOKEN_EXPIRE_MINUTES: int = int(os.environ.get("REFRESH_TOKEN_EXPIRE_MINUTES", 1440))
    
    # Image
    FILEPATH: str = "./static/images/" 
    

def get_settings() -> Settings: 
    return Settings()
