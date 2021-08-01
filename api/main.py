from .app import app

from starlette.responses import RedirectResponse

from api.routers import manga, chapter

app.include_router(manga.router)
app.include_router(chapter.router)


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse("/docs")


@app.get("/ping", tags=["Status"])
async def ping():
    """
    Ping the server
    """
    return "pong"
