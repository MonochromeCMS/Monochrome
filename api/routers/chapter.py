import os
import shutil

from typing import Optional, List
from uuid import UUID
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from .auth import is_connected, auth_responses
from ..exceptions import NotFoundHTTPException
from ..config import get_settings
from ..db import get_db
from ..models.chapter import Chapter
from ..schemas.chapter import ChapterSchema, ChapterResponse, LatestChaptersResponse, DetailedChapterResponse


global_settings = get_settings()

router = APIRouter(prefix="/chapter", tags=["Chapter"])


@router.get("", response_model=LatestChaptersResponse)
async def get_latest_chapters(
    limit: Optional[int] = Query(10, ge=1, le=100),
    offset: Optional[int] = Query(0, ge=0),
    db_session: AsyncSession = Depends(get_db),
):
    count, page = await Chapter.latest(db_session, limit, offset)
    return {
        "offset": offset,
        "limit": limit,
        "results": page,
        "total": count,
    }


get_responses = {
    200: {
        "description": "The requested chapter",
        "model": DetailedChapterResponse,
    },
    404: {
        "description": "The chapter couldn't be found",
        **NotFoundHTTPException.open_api("Chapter not found"),
    },
}


@router.get("/{id}", response_model=DetailedChapterResponse, responses=get_responses)
async def get_chapter(
    id: UUID,
    db_session: AsyncSession = Depends(get_db),
):
    return await Chapter.find_rel(db_session, id, Chapter.manga, NotFoundHTTPException("Chapter not found"))


delete_responses = {
    **auth_responses,
    **get_responses,
    200: {
        "description": "The chapter was deleted",
        "content": {
            "application/json": {
                "example": "OK",
            },
        },
    },
}


@router.delete("/{id}", dependencies=[Depends(is_connected)], responses=delete_responses)
async def delete_chapter(id: UUID, db_session: AsyncSession = Depends(get_db)):
    chapter = await Chapter.find(db_session, id, NotFoundHTTPException("Chapter not found"))
    shutil.rmtree(os.path.join(global_settings.media_path, str(chapter.manga_id), str(chapter.id)), True)
    return await Chapter.delete(chapter, db_session)


put_responses = {
    **auth_responses,
    **get_responses,
    200: {
        "description": "The edited chapter",
        "model": ChapterResponse,
    },
}


@router.put("/{id}", response_model=ChapterResponse, dependencies=[Depends(is_connected)], responses=put_responses)
async def update_chapter(
    payload: ChapterSchema,
    id: UUID,
    db_session: AsyncSession = Depends(get_db),
):
    chapter = await Chapter.find(db_session, id, NotFoundHTTPException("Chapter not found"))
    await chapter.update(db_session, **payload.dict())
    return chapter
