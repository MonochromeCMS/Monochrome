import os
import shutil

from typing import List, Tuple, Iterable
from PIL import Image

from uuid import UUID
from fastapi import APIRouter, Depends, File, UploadFile, status, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from .auth import is_connected, auth_responses
from ..exceptions import BadRequestHTTPException, NotFoundHTTPException
from ..config import get_settings
from ..db import get_db
from ..models.manga import Manga
from ..models.chapter import Chapter
from ..models.upload import UploadSession, UploadedBlob
from ..schemas.chapter import ChapterResponse
from ..schemas.upload import UploadSessionSchema, CommitUploadSession, UploadSessionResponse, UploadedBlobResponse

global_settings = get_settings()

router = APIRouter(prefix="/upload", tags=["Upload"], dependencies=[Depends(is_connected)])


def copy_chapter_to_session(chapter: Chapter, blobs: List[UUID]):
    chapter_path = os.path.join(global_settings.media_path, str(chapter.manga_id), str(chapter.id))
    blob_path = os.path.join(global_settings.media_path, "blobs")
    for i in range(chapter.length):
        shutil.copy(os.path.join(chapter_path, f"{i + 1}.jpg"), os.path.join(blob_path, f"{blobs[i]}.jpg"))


post_responses = {
    **auth_responses,
    404: {
        "description": "The manga/chapter couldn't be found",
        **NotFoundHTTPException.open_api("Manga/Chapter not found"),
    },
    400: {
        "description": "The chapter doesn't belong to that manga",
        **BadRequestHTTPException.open_api("The provided chapter doesn't belong to this manga"),
    },
    201: {
        "description": "The created session",
        "model": UploadSessionResponse,
    },
}


@router.post(
    "/begin", status_code=status.HTTP_201_CREATED, response_model=UploadSessionResponse, responses=post_responses
)
async def begin_upload_session(
    payload: UploadSessionSchema,
    db_session: AsyncSession = Depends(get_db),
):
    await Manga.find(db_session, payload.manga_id, NotFoundHTTPException("Manga not found"))
    if payload.chapter_id:
        chapter = await Chapter.find(db_session, payload.chapter_id, NotFoundHTTPException("Chapter not found"))
        if chapter.manga_id != payload.manga_id:
            raise BadRequestHTTPException("The provided chapter doesn't belong to this manga")

    session = UploadSession(**payload.dict())
    await session.save(db_session)

    if payload.chapter_id:
        blobs = []
        for i in range(1, chapter.length + 1):
            blob = UploadedBlob(session_id=session.id, name=f"{i}.jpg")
            await blob.save(db_session)
            blobs.append(blob.id)
        copy_chapter_to_session(chapter, blobs)

    return await UploadSession.find_rel(db_session, session.id, UploadSession.blobs)


get_responses = {
    **auth_responses,
    404: {
        "description": "The upload session couldn't be found",
        **NotFoundHTTPException.open_api("Session not found"),
    },
    200: {
        "description": "The requested upload session",
        "model": UploadSessionResponse,
    },
}


@router.get(
    "/{id}", response_model=UploadSessionResponse, dependencies=[Depends(is_connected)], responses=get_responses
)
async def get_upload_session(
    id: UUID,
    db_session: AsyncSession = Depends(get_db),
):
    session = await UploadSession.find_rel(
        db_session, id, UploadSession.blobs, NotFoundHTTPException("Session not found")
    )
    return session


def save_session_image(files: Iterable[Tuple[str, File]]):
    for blob_id, file in files:
        im = Image.open(file)
        im.convert("RGB").save(os.path.join(global_settings.media_path, "blobs", f"{blob_id}.jpg"))


post_blobs_responses = {
    **auth_responses,
    400: {"description": "An image isn't valid", **BadRequestHTTPException.open_api("file_name is not an image")},
    404: {
        "description": "The upload session couldn't be found",
        **NotFoundHTTPException.open_api("Session not found"),
    },
    201: {
        "description": "The created blobs",
        "model": List[UploadedBlobResponse],
    },
}


@router.post(
    "/{id}",
    status_code=status.HTTP_201_CREATED,
    response_model=List[UploadedBlobResponse],
    responses=post_blobs_responses,
)
async def upload_pages_to_upload_session(
    id: UUID,
    payload: List[UploadFile] = File(...),
    db_session: AsyncSession = Depends(get_db),
):
    for file in payload:
        if not file.content_type.startswith("image/"):
            raise BadRequestHTTPException(f"'{file.filename}' is not an image")

    session = await UploadSession.find(db_session, id, NotFoundHTTPException("Session not found"))

    blobs = []

    for file in payload:
        file_blob = UploadedBlob(session_id=session.id, name=file.filename)
        await file_blob.save(db_session)
        blobs.append(file_blob)

    save_session_image(zip((b.id for b in blobs), (f.file for f in payload)))

    return blobs


def delete_session_images(ids: List[UUID]):
    for blob_id in ids:
        os.remove(os.path.join(global_settings.media_path, "blobs", f"{blob_id}.jpg"))


delete_responses = {
    **get_responses,
    200: {
        "description": "The upload session was deleted",
        "content": {
            "application/json": {
                "example": "OK",
            },
        },
    },
}


@router.delete("/{id}", responses=delete_responses)
async def delete_upload_session(
    id: UUID,
    tasks: BackgroundTasks,
    db_session: AsyncSession = Depends(get_db),
):
    session = await UploadSession.find_rel(
        db_session, id, UploadSession.blobs, NotFoundHTTPException("Session not found")
    )
    session_images = (b.id for b in session.blobs)
    await session.delete(db_session)
    tasks.add_task(delete_session_images, session_images)
    return "OK"


def commit_session_images(chapter: Chapter, pages: List[UUID], edit: bool):
    blob_path = os.path.join(global_settings.media_path, "blobs")
    chapter_path = os.path.join(global_settings.media_path, str(chapter.manga_id), str(chapter.id))

    if edit:
        shutil.rmtree(chapter_path)
    os.mkdir(chapter_path)

    page_number = 1
    for page in pages:
        shutil.move(os.path.join(blob_path, f"{page}.jpg"), os.path.join(chapter_path, f"{page_number}.jpg"))
        page_number += 1


post_commit_responses = {
    **auth_responses,
    400: {
        "description": "There is a problem with the provided page order",
        **BadRequestHTTPException.open_api("Some pages don't belong to this session"),
    },
    404: {
        "description": "The session/chapter couldn't be found",
        **NotFoundHTTPException.open_api("Session/chapter not found"),
    },
    200: {
        "description": "The edited chapter",
        "model": ChapterResponse,
    },
    201: {
        "description": "The created chapter",
        "model": ChapterResponse,
    },
}


@router.post("/{id}/commit", response_model=ChapterResponse, responses=post_commit_responses)
async def commit_upload_session(
    id: UUID,
    payload: CommitUploadSession,
    tasks: BackgroundTasks,
    db_session: AsyncSession = Depends(get_db),
):
    session = await UploadSession.find_rel(
        db_session, id, UploadSession.blobs, NotFoundHTTPException("Session not found")
    )
    blobs = [b.id for b in session.blobs]
    edit = session.chapter_id is not None
    if not len(payload.page_order) > 0:
        raise BadRequestHTTPException("At least one page needs to be provided")
    if len(set(payload.page_order).difference(blobs)) > 0:
        raise BadRequestHTTPException("Some pages don't belong to this session")

    if session.chapter_id:
        chapter = await Chapter.find(db_session, session.chapter_id, NotFoundHTTPException("Chapter not found"))
        await chapter.update(db_session, length=len(payload.page_order), **payload.chapter_draft.dict())
    else:
        chapter = Chapter(manga_id=session.manga_id, length=len(payload.page_order), **payload.chapter_draft.dict())
        await chapter.save(db_session)

    await session.delete(db_session)
    tasks.add_task(commit_session_images, chapter, payload.page_order, edit)
    tasks.add_task(delete_session_images, set(blobs).difference(payload.page_order))
    content = jsonable_encoder(ChapterResponse.from_orm(chapter))
    return JSONResponse(status_code=(200 if edit else 201), content=content)


delete_blob_responses = {
    **get_responses,
    400: {
        "description": "That file doesn't exist in the provided upload session",
        **BadRequestHTTPException.open_api("The blob doesn't exist in the session"),
    },
    200: {
        "description": "The upload session was deleted",
        "content": {
            "application/json": {
                "example": "OK",
            },
        },
    },
}


@router.delete("/{session}/{file}", responses=delete_blob_responses)
async def delete_page_from_upload_session(
    session: UUID,
    file: UUID,
    tasks: BackgroundTasks,
    db_session: AsyncSession = Depends(get_db),
):
    session = await UploadSession.find_rel(
        db_session, session, UploadSession.blobs, NotFoundHTTPException("Session not found")
    )
    if file not in (b.id for b in session.blobs):
        raise BadRequestHTTPException("The blob doesn't exist in the session")

    blob = await UploadedBlob.find(db_session, file, NotFoundHTTPException("Blob not found"))
    await blob.delete(db_session)
    tasks.add_task(delete_session_images, (file,))
    return "OK"
