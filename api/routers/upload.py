import shutil

from typing import List, Tuple, Iterable
from os import path, makedirs, listdir, remove
from aiofiles import open
from pyunpack import Archive
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
    chapter_path = path.join(global_settings.media_path, str(chapter.manga_id), str(chapter.id))
    blob_path = path.join(global_settings.media_path, "blobs")
    for i in range(chapter.length):
        shutil.copy(path.join(chapter_path, f"{i + 1}.jpg"), path.join(blob_path, f"{blobs[i]}.jpg"))


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

    session_path = path.join(global_settings.temp_path, str(session.id))
    makedirs(path.join(session_path, "zip"))
    makedirs(path.join(session_path, "files"))

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


def save_session_image(files: Iterable[Tuple[str, str]]):
    for blob_id, file in files:
        im = Image.open(file)
        im.convert("RGB").save(path.join(global_settings.media_path, "blobs", f"{blob_id}.jpg"))
        remove(file)


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


def validate_image_extension(name: str):
    extensions = (".jpeg", ".jpg", ".png", ".bmp", ".webp")
    return any((name.lower().endswith(ext) for ext in extensions))


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
    compressed_formats = (
        "application/x-7z-compressed",
        "application/x-xz",
        "application/zip",
        "application/x-rar-compressed",
        "application/vnd.rar",
    )

    for file in payload:
        if file.content_type not in compressed_formats and not file.content_type.startswith("image/"):
            raise BadRequestHTTPException(f"'{file.filename}'s format is not supported")

    session = await UploadSession.find(db_session, id, NotFoundHTTPException("Session not found"))

    session_path = path.join(global_settings.temp_path, str(id))

    files_path = path.join(session_path, "files")

    blobs = []

    for file in payload:
        files = []
        file_blobs = []
        if file.content_type in compressed_formats:
            zip_path = path.join(session_path, f"zip/{file.filename}")
            async with open(zip_path, "wb") as out_file:
                content = await file.read()
                await out_file.write(content)

            Archive(zip_path).extractall(files_path, True)
            remove(zip_path)
            _files = listdir(files_path)
            files = [
                f for f in _files
                if path.isfile(path.join(files_path, f)) and validate_image_extension(f)
            ]
        else:
            async with open(path.join(files_path, file.filename), "wb") as out_file:
                content = await file.read()
                await out_file.write(content)
            files = (file.filename, )

        for f in files:
            file_blob = UploadedBlob(session_id=session.id, name=f)
            await file_blob.save(db_session)
            blobs.append(file_blob)
            file_blobs.append(file_blob.id)

        save_session_image(zip(file_blobs, (path.join(files_path, f) for f in files)))

    return blobs


def delete_session_images(ids: List[UUID]):
    for blob_id in ids:
        remove(path.join(global_settings.media_path, "blobs", f"{blob_id}.jpg"))


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
    session_path = path.join(global_settings.temp_path, str(session.id))
    tasks.add_task(shutil.rmtree, session_path, True)
    tasks.add_task(delete_session_images, session_images)
    return "OK"


def commit_session_images(chapter: Chapter, pages: List[UUID], edit: bool):
    blob_path = path.join(global_settings.media_path, "blobs")
    chapter_path = path.join(global_settings.media_path, str(chapter.manga_id), str(chapter.id))

    if edit:
        shutil.rmtree(chapter_path, True)
    makedirs(chapter_path, exist_ok=True)

    page_number = 1
    for page in pages:
        shutil.move(path.join(blob_path, f"{page}.jpg"), path.join(chapter_path, f"{page_number}.jpg"))
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

    session_path = path.join(global_settings.temp_path, str(session.id))
    tasks.add_task(shutil.rmtree, session_path, True)

    await session.delete(db_session)

    tasks.add_task(commit_session_images, chapter, payload.page_order, edit)
    tasks.add_task(delete_session_images, set(blobs).difference(payload.page_order))
    content = jsonable_encoder(ChapterResponse.from_orm(chapter))
    return JSONResponse(status_code=(200 if edit else 201), content=content)


delete_all_blobs_responses = {
    **get_responses,
    200: {
        "description": "All the uploaded images were deleted",
        "content": {
            "application/json": {
                "example": "OK",
            },
        },
    },
}


@router.delete("/{session}/files", responses=delete_all_blobs_responses)
async def delete_all_pages_from_upload_session(
    session: UUID,
    tasks: BackgroundTasks,
    db_session: AsyncSession = Depends(get_db),
):
    session = await UploadSession.find_rel(
        db_session, session, UploadSession.blobs, NotFoundHTTPException("Session not found")
    )

    session_images = (b.id for b in session.blobs)
    tasks.add_task(delete_session_images, session_images)

    for blob in session.blobs:
        blob_id = blob.id
        await blob.delete(db_session)

    return "OK"


delete_blob_responses = {
    **get_responses,
    400: {
        "description": "That file doesn't exist in the provided upload session",
        **BadRequestHTTPException.open_api("The blob doesn't exist in the session"),
    },
    200: {
        "description": "The uploaded image was deleted",
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
