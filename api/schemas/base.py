from typing import List
from pydantic import BaseModel, Field


class PaginationResponse(BaseModel):
    offset: int = Field(..., ge=0)
    limit: int = Field(..., ge=1, le=100)
    results: List
    total: int = Field(..., ge=0)
