import asyncio
from loguru import logger
from schemas.search import SearchResult
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
    response = await rag_chain.ainvoke(search)
    logger.info(response)

    return [
        SearchResult(
            title=f"Article #{i+1} {search}",
            page_content="Lorem Ipsum fdskfls " * 50,
            link="https://google.com",
        ) for i in range(20)
    ]
