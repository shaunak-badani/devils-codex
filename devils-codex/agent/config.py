import os
from functools import lru_cache
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-4o-mini-2024-07-18")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

@lru_cache()
def get_settings() -> Settings:
    return Settings()