import sys
import os
from loguru import logger
from typing import Dict, Any
from pydantic_settings import BaseSettings
import requests

class Settings(BaseSettings):
    log_level: str = os.getenv("LOG_LEVEL", "DEBUG")
    page_size: int = int(os.getenv("PAGE_SIZE", "5"))

    llm_model_id: str = os.getenv("MODEL_ID", "llama-2-70b-chat-hf")
    
    openai_api_service: str = os.getenv("OPENAI_API_SERVICE", "local") # local | rapid | openai
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "test")
    openai_api_base: str
    rapid_client_id: str
    rapid_client_secret: str

    # Directus settings
    directus_host: str = os.getenv("DIRECTUS_HOST", "http://directus:8055")
    directus_api_key: str = "btFBH6DZzvhfufNYakQOmozszmFtEByj"
    directus_rag_feedback_table: str = os.getenv("DIRECTUS_RAG_FEEDBACK_TABLE", "ai_rag_feedback")
    directus_search_feedback_table: str = os.getenv("DIRECTUS_RAG_FEEDBACK_TABLE", "ai_search_feedback")

    # Define score mappings for both "thumbs" and "faces" feedback systems
    score_mappings: Dict[str, Any] = {
        "thumbs": {"👍": 1, "👎": 0},
        "faces": {"😀": 1, "🙂": 0.75, "😐": 0.5, "🙁": 0.25, "😞": 0},
    }

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
