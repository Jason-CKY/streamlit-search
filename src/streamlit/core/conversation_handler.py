from langchain_core.documents import Document
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.messages import (
    SystemMessage,
)
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.prompts.prompt import PromptTemplate
from loguru import logger
from typing import List
from pydantic import BaseModel

class ConversationHandler(BaseModel):
    model: str
    query: str
    temperature: float = 0
    max_tokens: int = 1024
    api_token: str = "EMPTY"

    def _get_rag_chain(self):
        qa_prompt = self._get_qa_prompt()
        model_context_length = get_model_information(self.model, self._token)["loader_params"]["max_context_length"]

        _llm = self._get_llm()
        
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
        
        # count tokens and drop documents beyond a token count
        def format_docs(documents_and_scores):
            documents = [document for (document, _) in documents_and_scores]
            max_tokens_limit=_model_context_length - self._max_tokens - 10
            return "\n\n".join(doc.page_content for doc in _reduce_tokens_below_limit(max_tokens_limit, documents, _llm))

        rag_chain_from_docs = (
            RunnablePassthrough.assign(context=(lambda x: format_docs(x["context"])))
            | _qa_prompt
            | _llm
            | StrOutputParser()
        )

        rag_chain_with_source = RunnableParallel(
            {"context": _retriever, "question": RunnablePassthrough()}
        ).assign(answer=rag_chain_from_docs)

        return rag_chain_with_source

    def _get_llm(self, callback_manager = None):
        """Constructs a LLM instance based on the configured OpenAI API service."""
        if settings.openai_api_service == "rapid":
            from internal_llm_tools.llms import RAPIDChatOpenAI

            logger.debug("Initializing ChatOpenAI using 'RAPIDChatOpenAI'")
            return RAPIDChatOpenAI(
                model_name=self._model_name,
                temperature=self._temperature,
                streaming=self._stream,
                max_tokens=self._max_tokens,
                # openai_api_key=self._token, # we use service account to call due to long embedding time
                openai_api_base=f"{settings.openai_api_base}",
                http_client=openai_async_client,
                callback_manager=callback_manager
            )
        elif settings.openai_api_service == "local":
            from app.core.dev_dependencies import LocalChatOpenAI

            logger.debug("Initializing ChatOpenAI using 'LocalChatOpenAI'")
            return LocalChatOpenAI(
                temperature=self._temperature,
                model_name=self._model_name,
                streaming=self._stream,
                openai_api_key=self._token,
                openai_api_base=f"{settings.openai_api_base}",
                max_tokens=self._max_tokens,
                callback_manager=callback_manager
            )
        elif settings.openai_api_service == "openai":
            from langchain.chat_models import ChatOpenAI

            logger.debug("Initializing ChatOpenAI using 'ChatOpenAI'")
            return ChatOpenAI(
                temperature=self._temperature, 
                streaming=self._stream,
                callback_manager=callback_manager
            )
        else:
            logger.error(f"OpenAI API service '{settings.openai_api_service}' not supported.")
            return None

    def _get_conversation_inputs(self):
        """Gets the inputs needed for a conversational search."""
        qa_prompt = self._get_qa_prompt()

        model_context_length = get_model_information(self._model_name, self._token)["loader_params"]["max_context_length"]
        logger.debug(f"Context length '{model_context_length}' for '{self._model_name}'")

        return qa_prompt, model_context_length

    def _get_qa_prompt(self):
        """Constructs the prompt to use for question answering."""
        messages = []
        qa_prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Question: {question}
Helpful Answer:"""
        if self._system_prompt is not None:
            messages.append(SystemMessage(content=self._system_prompt))
        messages.append(HumanMessagePromptTemplate(prompt=PromptTemplate.from_template(qa_prompt_template)))
        qa_prompt = ChatPromptTemplate.from_messages(messages)
        logger.debug(f"Prompt template '{qa_prompt}'")
        return qa_prompt
