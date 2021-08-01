import logging

from fastapi import FastAPI

from .db import engine

log = logging.getLogger(__name__)

app = FastAPI(title="Monochrome", version="0.1")


async def stop_db():
    await engine.dispose()


@app.on_event("startup")
async def startup_event():
    log.info("Starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")
    await stop_db()
