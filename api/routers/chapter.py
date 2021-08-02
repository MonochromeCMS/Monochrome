import os
import shutil

from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import get_settings
from ..db import get_db
from ..models.chapter import Chapter
from ..schemas.chapter import ChapterSchema, ChapterResponse


global_settings = get_settings()

router = APIRouter(prefix="/chapter", tags=["Chapter"])


@router.get("/{id}", response_model=ChapterResponse)
async def get_chapter(
    id: UUID,
    db_session: AsyncSession = Depends(get_db),
):
    return await Chapter.find(db_session, id)


@router.delete("/{id}")
async def delete_chapter(id: UUID, db_session: AsyncSession = Depends(get_db)):
    chapter = await Chapter.find(db_session, id)
    shutil.rmtree(os.path.join(global_settings.media_path, str(chapter.manga_id), str(chapter.id)))
    return await Chapter.delete(chapter, db_session)


@router.put("/{id}", response_model=ChapterResponse)
async def update_chapter(
    payload: ChapterSchema,
    id: UUID,
    db_session: AsyncSession = Depends(get_db),
):
    chapter = await Chapter.find(db_session, id)
    await chapter.update(db_session, **payload.dict())
    return chapter
