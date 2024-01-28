from pydantic import BaseModel
from typing import Optional, Callable, Any, List, Optional

class PaginationButton(BaseModel):
    text: str
    onClick: Callable
    args: Optional[List[Any]]
    disabled: bool = False
