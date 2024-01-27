from loguru import logger
from core.settings import settings, requests_session

def get_model_information(model_name):
    if settings.openai_api_service == "openai":
        # default gpt-3.5-turbo context length
        return {
            "model_id": "gpt-3.5-turbo",
            "revision": None,
            "loader_params": {
                "max_context_length": 4096
            },
            "tokenizer_params": {
                "model_id": "gpt-3.5-turbo",
                "revision": None
            }
        }
    response = requests_session.get(
            f"{settings.openai_api_base}/model/{model_name}",
            verify=False,
        )
    if response.status_code != 200:
        logger.error(response.text)
        return None
    return response.json()
