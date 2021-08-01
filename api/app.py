import logging
import os
from shutil import rmtree

from fastapi import FastAPI

from .models.upload import UploadSession

from .db import engine, get_db
from .config import get_settings

global_settings = get_settings()

log = logging.getLogger(__name__)

app = FastAPI(title="Monochrome", version="0.1")


async def setup_media():
    async for session in get_db():
        await UploadSession.flush(session)

    rmtree(os.path.join(global_settings.media_path, "blobs"), ignore_errors=True)
    os.mkdir(os.path.join(global_settings.media_path, "blobs"))


async def stop_db():
    await engine.dispose()


@app.on_event("startup")
async def startup_event():
    log.info("Starting up...")
    await setup_media()


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")
    await stop_db()
