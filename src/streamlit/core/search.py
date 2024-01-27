import asyncio
from loguru import logger
from schemas.search import SearchResult
from langchain_core.documents import Document
from core.conversation_handler import ConversationHandler
from core.settings import settings

async def mock_search_results(search: str):
    await asyncio.sleep(1)
    handler = ConversationHandler(
        model = settings.model_id,
        temperature = 0,
        max_tokens = 1024,
    )
    rag_chain = handler.get_rag_chain()
    source_documents = [
        Document(
            page_content="test from source document", 
            metadata={
                "source_document": "https://google.com"
            }
        )
    ]
    response = await rag_chain.ainvoke({
        "context": handler.format_docs(source_documents),
        "question": search,
    })
    logger.info(response)

    return [
        SearchResult(
            title=f"Article #{i+1} {search}",
            page_content="Lorem Ipsum fdskfls " * 50,
            link="https://google.com",
        ) for i in range(20)
    ]
