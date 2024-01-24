from pydantic import BaseModel
from typing import Optional

class SearchResult(BaseModel):
    title: str
    page_content: str
    link: Optional[str]
