import os
import shutil

from PIL import Image

from uuid import UUID
from typing import Optional, List
from fastapi import APIRouter, Depends, status, Query, File, UploadFile, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from .auth import is_connected
from ..exceptions import BadRequestHTTPException
from ..config import get_settings
from ..db import get_db
from ..models.chapter import Chapter
from ..models.manga import Manga
from ..schemas.chapter import ChapterResponse
from ..schemas.manga import MangaSchema, MangaResponse, MangaSearchResponse


global_settings = get_settings()

router = APIRouter(prefix="/manga", tags=["Manga"])


@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=MangaResponse, dependencies=[Depends(is_connected)]
)
async def create_manga(payload: MangaSchema, db_session: AsyncSession = Depends(get_db)):
    manga = Manga(**payload.dict())
    await manga.save(db_session)
    os.mkdir(os.path.join(global_settings.media_path, str(manga.id)))
    return manga


@router.get("", response_model=MangaSearchResponse)
async def search_manga(
    title: str = "",
    limit: Optional[int] = Query(10, ge=1, le=100),
    offset: Optional[int] = Query(0, ge=0),
    db_session: AsyncSession = Depends(get_db),
):
    count, page = await Manga.search(db_session, title, limit, offset)
    return {
        "offset": offset,
        "limit": limit,
        "results": page,
        "total": count,
    }


@router.get("/{id}", response_model=MangaResponse)
async def get_manga(
    id: UUID,
    db_session: AsyncSession = Depends(get_db),
):
    return await Manga.find(db_session, id)


@router.get("/{id}/chapters", response_model=List[ChapterResponse])
async def get_manga_chapters(
    id: UUID,
    db_session: AsyncSession = Depends(get_db),
):
    await Manga.find(db_session, id)
    return await Chapter.from_manga(db_session, id)


@router.delete("/{id}", dependencies=[Depends(is_connected)])
async def delete_manga(id: UUID, db_session: AsyncSession = Depends(get_db)):
    manga = await Manga.find(db_session, id)
    shutil.rmtree(os.path.join(global_settings.media_path, str(manga.id)))
    return await Manga.delete(manga, db_session)


@router.put("/{id}", response_model=MangaResponse, dependencies=[Depends(is_connected)])
async def update_manga(
    payload: MangaSchema,
    id: UUID,
    db_session: AsyncSession = Depends(get_db),
):
    manga = await Manga.find(db_session, id)
    await manga.update(db_session, **payload.dict())
    return manga


def save_cover(manga_id: UUID, file: File):
    im = Image.open(file)
    im.convert("RGB").save(os.path.join(global_settings.media_path, str(manga_id), "cover.jpg"))


@router.put("/{id}/cover", dependencies=[Depends(is_connected)])
async def set_manga_cover(
    id: UUID,
    tasks: BackgroundTasks,
    payload: UploadFile = File(...),
    db_session: AsyncSession = Depends(get_db),
):
    if not payload.content_type.startswith("image/"):
        raise BadRequestHTTPException(f"'{payload.filename}' is not an image")

    manga = await Manga.find(db_session, id)
    tasks.add_task(save_cover, manga.id, payload.file)
    return manga
