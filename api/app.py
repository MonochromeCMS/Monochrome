import logging
from os import makedirs, path
from shutil import rmtree

from fastapi import FastAPI, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from .models.upload import UploadSession

from .db import engine, get_db
from .config import get_settings

global_settings = get_settings()

log = logging.getLogger(__name__)

app = FastAPI(title="Monochrome", version="1.2.0")


def get_remote_address(request: Request):
    ip = (
        request.headers.get("CF-CONNECTING-IP")
        or request.headers.get("X-FORWARDED-FOR")
        or request.client.host
        or "127.0.0.1"
    )
    return ip


limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)


async def setup_media():
    async for session in get_db():
        await UploadSession.flush(session)

    rmtree(path.join(global_settings.media_path, "blobs"), ignore_errors=True)
    makedirs(path.join(global_settings.media_path, "blobs"), exist_ok=True)


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
