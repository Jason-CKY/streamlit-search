import sys
import os
from loguru import logger
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    log_level: str = os.getenv("LOG_LEVEL", "DEBUG")
    page_size: int = int(os.getenv("PAGE_SIZE", "5"))
    openai_api_service: str = os.getenv("OPENAI_API_SERVICE", "local") # local or rapid

settings = Settings()

logger.remove()
logger.add(sys.stdout, level=settings.log_level)
