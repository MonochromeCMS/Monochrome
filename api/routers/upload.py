import os
import shutil

from typing import List, Tuple
from PIL import Image

from uuid import UUID
from fastapi import APIRouter, Depends, File, UploadFile, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from ..exceptions import BadRequestHTTPException
from ..config import get_settings
from ..db import get_db
from ..models.manga import Manga
from ..models.chapter import Chapter
from ..models.upload import UploadSession, UploadedBlob
from ..schemas.chapter import ChapterResponse
from ..schemas.upload import BeginUploadSession, CommitUploadSession, UploadSessionResponse, UploadedBlobResponse

global_settings = get_settings()

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post("/begin", status_code=status.HTTP_201_CREATED, response_model=UploadSessionResponse)
async def begin_upload_session(
    payload: BeginUploadSession,
    db_session: AsyncSession = Depends(get_db),
):
    await Manga.find(db_session, payload.manga_id)
    session = UploadSession(**payload.dict())
    await session.save(db_session)
    return await UploadSession.find_rel(db_session, session.id, UploadSession.blobs)


@router.get("/{id}", response_model=UploadSessionResponse)
async def get_upload_session(
    id: UUID,
    db_session: AsyncSession = Depends(get_db),
):
    session = await UploadSession.find_rel(db_session, id, UploadSession.blobs)
    return session


def save_session_image(files: List[Tuple[str, File]]):
    for blob_id, file in files:
        im = Image.open(file)
        im.convert("RGB").save(os.path.join(global_settings.media_path, "blobs", f"{blob_id}.jpg"))


@router.post("/{id}", status_code=status.HTTP_201_CREATED, response_model=List[UploadedBlobResponse])
async def upload_pages_to_upload_session(
    id: UUID,
    tasks: BackgroundTasks,
    payload: List[UploadFile] = File(...),
    db_session: AsyncSession = Depends(get_db),
):
    for file in payload:
        if not file.content_type.startswith("image/"):
            raise BadRequestHTTPException(f"'{file.filename}' is not an image")

    session = await UploadSession.find(db_session, id)

    blobs = []

    for file in payload:
        file_blob = UploadedBlob(session_id=session.id, name=file.filename)
        await file_blob.save(db_session)
        blobs.append(file_blob)

    tasks.add_task(save_session_image, zip((b.id for b in blobs), (f.file for f in payload)))
    return blobs


def delete_session_images(ids: List[UUID]):
    for blob_id in ids:
        os.remove(os.path.join(global_settings.media_path, "blobs", f"{blob_id}.jpg"))


@router.delete("/{id}")
async def delete_upload_session(
    id: UUID,
    tasks: BackgroundTasks,
    db_session: AsyncSession = Depends(get_db),
):
    session = await UploadSession.find_rel(db_session, id, UploadSession.blobs)
    session_images = (b.id for b in session.blobs)
    await session.delete(db_session)
    tasks.add_task(delete_session_images, session_images)
    return True


def commit_session_images(manga_id: UUID, chapter_id: UUID, pages: List[UUID]):
    blob_path = os.path.join(global_settings.media_path, "blobs")
    chapter_path = os.path.join(global_settings.media_path, str(manga_id), str(chapter_id))
    page_number = 1
    for page in pages:
        shutil.move(os.path.join(blob_path, f"{page}.jpg"), os.path.join(chapter_path, f"{page_number}.jpg"))
        page_number += 1


@router.post("/{id}/commit", response_model=ChapterResponse, status_code=status.HTTP_201_CREATED)
async def commit_upload_session(
    id: UUID,
    payload: CommitUploadSession,
    tasks: BackgroundTasks,
    db_session: AsyncSession = Depends(get_db),
):
    session = await UploadSession.find_rel(db_session, id, UploadSession.blobs)
    blobs = (b.id for b in session.blobs)
    if not len(payload.page_order) > 0:
        raise BadRequestHTTPException("At least one page needs to be provided")
    if len(set(payload.page_order).difference(blobs)) > 0:
        raise BadRequestHTTPException("Some pages provided don't belong to this session.")

    chapter = Chapter(manga_id=session.manga_id, length=len(payload.page_order), **payload.chapterDraft.dict())
    await chapter.save(db_session)
    await session.delete(db_session)
    os.mkdir(os.path.join(global_settings.media_path, str(chapter.manga_id), str(chapter.id)))
    tasks.add_task(commit_session_images, chapter.manga_id, chapter.id, payload.page_order)
    tasks.add_task(delete_session_images, set(blobs).difference(payload.page_order))
    return chapter


@router.delete("/{session}/{file}")
async def delete_page_from_upload_session(
    session: UUID,
    file: UUID,
    tasks: BackgroundTasks,
    db_session: AsyncSession = Depends(get_db),
):
    session = await UploadSession.find_rel(db_session, session, UploadSession.blobs)
    if file not in (b.id for b in session.blobs):
        raise BadRequestHTTPException("That file doesn't exist in the provided upload session")

    blob = await UploadedBlob.find(db_session, file)
    await blob.delete(db_session)
    tasks.add_task(delete_session_images, (file,))
    return True
