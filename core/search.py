import asyncio
from schemas.search import SearchResult

async def mock_search_results(search: str):
    await asyncio.sleep(2)
    return [
        SearchResult(
            title=f"Article #{i+1} {search}",
            page_content="Lorem Ipsum fdskfls " * 50,
            link="https://google.com",
        ) for i in range(20)
    ]
