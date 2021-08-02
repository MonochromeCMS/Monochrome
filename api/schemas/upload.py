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


class UploadSessionResponse(BeginUploadSession):
    id: UUID = Field(
        description="ID of the upload session",
    )
    blobs: List = Field(
        (),
        description="Images uploaded to the session",
    )

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "manga_id": "1e01d7f6-c4e1-4102-9dd0-a6fccc065978",
                "id": "73c981e6-4267-4f35-8e41-0d124ebcb6a2",
            }
        }


class CommitUploadSession(BaseModel):
    chapterDraft: ChapterSchema = Field(description="Details of the chapter")
    page_order: List[UUID] = Field(description="Order the pages should be uploaded in")
