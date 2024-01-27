from loguru import logger
from core.settings import settings, requests_session

def get_model_information(model_name):
    response = requests_session.get(
            f"{settings.openai_api_base}/model/{model_name}",
            verify=False,
        )
    if response.status_code != 200:
        logger.error(response.text)
        return None
    return response.json()
