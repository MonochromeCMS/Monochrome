from uuid import UUID
from typing import List, Optional
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_db
from ..models.manga import Manga
from ..schemas.manga import MangaSchema, MangaResponse, SearchResponse

router = APIRouter(prefix="/manga", tags=["Manga"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=MangaResponse)
async def create_manga(payload: MangaSchema, db_session: AsyncSession = Depends(get_db)):
    manga = Manga(**payload.dict())
    await manga.save(db_session)
    return manga


@router.get("", response_model=SearchResponse)
async def search_manga(
    title: str,
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


@router.delete("/{id}")
async def delete_manga(id: UUID, db_session: AsyncSession = Depends(get_db)):
    manga = await Manga.find(db_session, id)
    return await Manga.delete(manga, db_session)


@router.put("/{id}", response_model=MangaResponse)
async def update_manga(
    payload: MangaSchema,
    id: UUID,
    db_session: AsyncSession = Depends(get_db),
):
    manga = await Manga.find(db_session, id)
    await manga.update(db_session, **payload.dict())
    return manga
