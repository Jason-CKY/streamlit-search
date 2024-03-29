from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.prompts.prompt import PromptTemplate
from loguru import logger
from typing import List
from pydantic import BaseModel

from core.dependencies import get_model_information
from core.settings import settings, openai_async_client

class ConversationHandler(BaseModel):
    model: str
    temperature: float = 0
    max_tokens: int = 1024
    api_token: str = "EMPTY"

    def format_docs(self, documents: List[Document]):
        llm = self._get_llm()
        model_context_length = get_model_information(self.model)["loader_params"]["max_context_length"]

        def _reduce_tokens_below_limit(max_tokens_limit: int, docs: List[Document], llm) -> List[Document]:
            num_docs = len(docs)

            tokens = [
                llm.get_num_tokens(doc.page_content)
                for doc in docs
            ]
            token_count = sum(tokens[:num_docs])
            while token_count > max_tokens_limit:
                num_docs -= 1
                token_count -= tokens[num_docs]

            return docs[:num_docs]
        
        max_tokens_limit = model_context_length - self.max_tokens - 10
        return "\n\n".join(doc.page_content for doc in _reduce_tokens_below_limit(max_tokens_limit, documents, llm))

    def get_rag_chain(self):
        qa_prompt = self._get_qa_prompt()
        llm = self._get_llm()

        rag_chain_from_docs = (
            qa_prompt
            | llm
            | StrOutputParser()
        )

        return rag_chain_from_docs

    def _get_llm(self, callback_manager = None):
        """Constructs a LLM instance based on the configured OpenAI API service."""
        if settings.openai_api_service == "rapid":
            from internal_llm_tools.llms import RAPIDChatOpenAI

            logger.debug("Initializing ChatOpenAI using 'RAPIDChatOpenAI'")
            return RAPIDChatOpenAI(
                model_name=self.model,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                openai_api_base=f"{settings.openai_api_base}",
                http_client=openai_async_client,
                callback_manager=callback_manager
            )
        elif settings.openai_api_service == "local":
            from core.dev_dependencies import LocalChatOpenAI

            logger.debug("Initializing ChatOpenAI using 'LocalChatOpenAI'")
            return LocalChatOpenAI(
                temperature=self.temperature,
                model_name=self.model,
                openai_api_key=settings.openai_api_key,
                openai_api_base=settings.openai_api_base,
                max_tokens=self.max_tokens,
                callback_manager=callback_manager
            )
        elif settings.openai_api_service == "openai":
            from langchain_community.chat_models import ChatOpenAI

            logger.debug("Initializing ChatOpenAI using 'ChatOpenAI'")
            return ChatOpenAI(
                temperature=self._temperature, 
                streaming=self._stream,
                max_tokens=self.max_tokens,
                openai_api_key=settings.openai_api_key,
                openai_api_base=settings.openai_api_base,
                callback_manager=callback_manager
            )
        else:

            logger.error(f"OpenAI API service '{settings.openai_api_service}' not supported.")
            return None

    def _get_qa_prompt(self):
        """Constructs the prompt to use for question answering."""
        messages = []
        qa_prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Question: {question}
Helpful Answer:"""
        messages.append(HumanMessagePromptTemplate(prompt=PromptTemplate.from_template(qa_prompt_template)))
        qa_prompt = ChatPromptTemplate.from_messages(messages)
        logger.debug(f"Prompt template '{qa_prompt}'")
        return qa_prompt
