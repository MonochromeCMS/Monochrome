from typing import Optional, List
from uuid import UUID
from datetime import datetime

from ..models.manga import Status
from .base import PaginationResponse

from pydantic import BaseModel, Field


class MangaSchema(BaseModel):
    title: str = Field(description="Title of the manga")
    description: str = Field(
        description="Short description of the manga",
    )
    author: str = Field(
        description="Author of the manga",
    )
    artist: str = Field(
        description="Artist of the manga",
    )
    year: Optional[int] = Field(
        None,
        description="Year of release of the manga",
    )
    status: Status = Field(
        description="Status of the manga",
    )

    class Config:
        schema_extra = {
            "example": {
                "title": "Monochrome Lovers",
                "description": "One day, suddenly, an angel came descending from the sky!?",
                "author": "Hibiki Mio",
                "artist": "Hibiki Mio",
                "year": 2021,
                "status": Status.ongoing,
            }
        }


class MangaResponse(MangaSchema):
    id: UUID = Field(
        title="ID",
        description="ID of the manga",
    )
    version: int = Field(
        description="Version of the manga",
    )
    create_time: datetime = Field(
        description="Time this manga was created",
    )

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "1e01d7f6-c4e1-4102-9dd0-a6fccc065978",
                "title": "Monochrome Lovers",
                "description": "One day, suddenly, an angel came descending from the sky!?",
                "author": "Hibiki Mio",
                "artist": "Hibiki Mio",
                "year": 2021,
                "status": Status.ongoing,
                "version": 2,
            }
        }


class SearchResponse(PaginationResponse):
    results: List[MangaResponse]
