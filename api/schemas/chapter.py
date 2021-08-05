from typing import Optional, List
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field

from .base import PaginationResponse
from .manga import MangaResponse


class ChapterSchema(BaseModel):
    name: str = Field(description="Name of the chapter")
    volume: Optional[int] = Field(
        description="Volume this chapter comes from",
    )
    number: str = Field(description="Number of the chapter", regex="[0-9.]+")

    class Config:
        schema_extra = {
            "example": {
                "name": "A World That Won't Reject Me",
                "volume": None,
                "number": "19.5",
            }
        }


class ChapterResponse(ChapterSchema):
    id: UUID = Field(
        title="ID",
        description="ID of the manga",
    )
    version: int = Field(
        description="Version of the chapter",
    )
    manga_id: UUID = Field(
        description="Manga this chapter comes from",
    )
    length: int = Field(
        description="Amount of pages of the chapter",
        ge=1,
    )
    upload_time: datetime = Field(
        description="Time this chapter was uploaded",
    )

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "A World That Won't Reject Me",
                "volume": None,
                "number": "19.5",
                "length": 15,
                "manga_id": "1e01d7f6-c4e1-4102-9dd0-a6fccc065978",
                "version": 2,
                "id": "4abe53f4-0eaa-4f31-9210-a625fa665e23",
            }
        }


class DetailedChapterResponse(ChapterResponse):
    manga: MangaResponse


class LatestChaptersResponse(PaginationResponse):
    results: List[DetailedChapterResponse]
