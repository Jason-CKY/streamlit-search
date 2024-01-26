import requests
from loguru import logger
from core.settings import settings

def get_model_information(model_name, token: str = None):
    if settings.openai_api_service == "rapid":
        response = rapid_client_session.get(
            f"{settings.openai_api_base}/model/{model_name}",
            verify=False,
        )
    elif settings.openai_api_service == "local":
        response = requests.get(
            f"{settings.openai_api_base}/model/{model_name}",
            verify=False,
            headers={"Authorization": f"Bearer {token}"}
        )
    if response.status_code != 200:
        logger.error(response.text)
        return None
    return response.json()
