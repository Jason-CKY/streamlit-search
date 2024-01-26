from pydantic import BaseModel
from typing import Optional, Callable, Any, List, Optional

class SearchResult(BaseModel):
    title: str
    page_content: str
    link: Optional[str]

class PaginationButton(BaseModel):
    text: str
    onClick: Callable
    args: Optional[List[Any]]
    disabled: bool = False
