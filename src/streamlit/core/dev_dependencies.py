import requests
from langchain.adapters.openai import convert_message_to_dict
from langchain.chat_models import ChatOpenAI
from langchain.schema.messages import BaseMessage
from typing import List, Dict, Any, Optional, Union, Tuple

class LocalChatOpenAI(ChatOpenAI):
    requests.packages.urllib3.disable_warnings()
    model_name: str
    temperature: float
    model_kwargs: Dict[str, Any]
    openai_api_key: Optional[str] = "EMPTY"
    openai_api_base: Optional[str] = None
    openai_organization: Optional[str] = None
    openai_proxy: Optional[str] = None
    request_timeout: Optional[Union[float, Tuple[float, float]]] = None
    max_retries: int = 6
    streaming: bool = False
    n: int = 1
    max_tokens: Optional[int] = None

    def __init__(self, **data):
        super().__init__(**data)

    def num_tokens_request(self, text: str, model_name: str, max_tokens: int = 1024):
        if self.openai_api_key != "EMPTY":
            resp = requests.post(
                f"{self.openai_api_base}/token_check",
                verify=False,
                headers={"Authorization": f"Bearer {self.openai_api_key}"},
                json={
                    "prompts": [
                        {"model": model_name, "prompt": text, "max_tokens": max_tokens}
                    ]
                },
            )
        else:
            resp = requests.post(
                f"{self.openai_api_base}/token_check",
                verify=False,
                json={
                    "prompts": [
                        {"model": model_name, "prompt": text, "max_tokens": max_tokens}
                    ]
                },
            )
        if resp.status_code != 200:
            raise AssertionError(
                "Sorry, something went wrong with your request, please try again."
                + resp.text
            )
        return resp.json()["prompts"][0]["tokenCount"]

    def _get_encoding_model(self):
        raise NotImplementedError

    def get_token_ids(self, text: str) -> List[int]:
        raise NotImplementedError

    def get_num_tokens(self, text: str) -> int:
        response = self.num_tokens_request(text, self.model_name)
        return response

    def get_num_tokens_from_messages(self, messages: List[BaseMessage]) -> int:
        num_tokens = 0
        messages_dict = [convert_message_to_dict(m) for m in messages]
        for message in messages_dict:
            for _, value in message.items():
                num_tokens += self.get_num_tokens(str(value))
        return num_tokens
