from typing import List
from pydantic import BaseModel, Field

from ..config import get_settings

settings = get_settings()


class PaginationResponse(BaseModel):
    offset: int = Field(..., ge=0)
    limit: int = Field(..., ge=1, le=settings.max_page_limit)
    results: List
    total: int = Field(..., ge=0)

    class Config:
        orm_mode = True
