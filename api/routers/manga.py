from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_db
from ..models.manga import Manga
from ..schemas.manga import MangaSchema, MangaResponse

router = APIRouter(prefix="/manga")


@router.post("", status_code=status.HTTP_201_CREATED, response_model=MangaResponse)
async def create_stuff(payload: MangaSchema, db_session: AsyncSession = Depends(get_db)):
    manga = Manga(**payload.dict())
    await manga.save(db_session)
    return manga


@router.get("/{id}", response_model=MangaResponse)
async def find_stuff(
    id: UUID,
    db_session: AsyncSession = Depends(get_db),
):
    return await Manga.find(db_session, id)


@router.delete("/{id}")
async def delete_stuff(id: UUID, db_session: AsyncSession = Depends(get_db)):
    stuff = await Manga.find(db_session, id)
    return await Manga.delete(stuff, db_session)


@router.put("/{id}", response_model=MangaResponse)
async def update_stuff(
    payload: MangaSchema,
    id: UUID,
    db_session: AsyncSession = Depends(get_db),
):
    manga = await Manga.find(db_session, id)
    await manga.update(db_session, **payload.dict())
    return manga
