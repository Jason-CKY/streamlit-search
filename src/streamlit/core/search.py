import asyncio
import random
from typing import List
from loguru import logger
from schemas.search import SearchResult
from langchain_core.documents import Document
from core.conversation_handler import ConversationHandler
from core.settings import settings

async def mock_get_source_documents(search: str):
    await asyncio.sleep(random.random() * 2)
    return [
        SearchResult(
            title=f"Article #{i+1} {search}",
            page_content="Lorem Ipsum fdskfls " * 50,
            link="https://google.com",
        ) for i in range(20)
    ]

async def get_rag_response(search_query: str, source_documents: List[Document]) -> str:
    await asyncio.sleep(random.random() * 2)
    handler = ConversationHandler(
        model = settings.model_id,
        temperature = 0,
        max_tokens = 1024,
    )
    rag_chain = handler.get_rag_chain()
    response = await rag_chain.ainvoke({
        "context": handler.format_docs(source_documents),
        "question": search_query,
    })
    logger.info(response)
    return response


