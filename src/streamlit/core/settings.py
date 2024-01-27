import sys
import os
from loguru import logger
from pydantic_settings import BaseSettings
import requests

class Settings(BaseSettings):
    log_level: str = os.getenv("LOG_LEVEL", "DEBUG")
    page_size: int = int(os.getenv("PAGE_SIZE", "5"))

    model_id: str = os.getenv("MODEL_ID", "llama-2-70b-chat-hf")
    
    openai_api_service: str = os.getenv("OPENAI_API_SERVICE", "local") # local or rapid
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "test")
    openai_api_base: str
    rapid_client_id: str
    rapid_client_secret: str

settings = Settings()

try:
    from internal_llm_tools.utils.requests_rapid import RapidClientSession
    from internal_llm_tools.sessions import SyncRapidClient, AsyncRapidClient

    requests_session = RapidClientSession(
        settings.rapid_client_id, settings.rapid_client_secret
    )
    openai_sync_client = SyncRapidClient(verify=False)
    openai_async_client = AsyncRapidClient(verify=False)
except ImportError:
    requests_session = requests.Session()
    requests_session.headers = {
            "Authorization": "Bearer test",
    }
    openai_sync_client = None
    openai_async_client = None
    logger.error(f"Import error for RapidClientSession")


logger.remove()
logger.add(sys.stdout, level=settings.log_level)
