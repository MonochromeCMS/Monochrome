from typing import List
from uuid import UUID

from pydantic import BaseModel, Field

from .chapter import ChapterSchema


class BeginUploadSession(BaseModel):
    manga_id: UUID = Field(
        description="Manga this session is linked to",
    )

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "manga_id": "1e01d7f6-c4e1-4102-9dd0-a6fccc065978",
            }
        }


class UploadedBlobResponse(BaseModel):
    id: UUID = Field(
        description="ID of the uploaded blob",
    )
    name: str = Field(
        description="Name the blob was uploaded as",
    )

    class Config:
        orm_mode = True


class UploadSessionResponse(BeginUploadSession):
    id: UUID = Field(
        description="ID of the upload session",
    )
    blobs: List[UploadedBlobResponse] = Field(
        (),
        description="Images uploaded to the session",
    )

    class Config:
        orm_mode = True


class CommitUploadSession(BaseModel):
    chapterDraft: ChapterSchema = Field(description="Details of the chapter")
    page_order: List[UUID] = Field(description="Order the pages should be uploaded in")

    class Config:
        orm_mode = True
