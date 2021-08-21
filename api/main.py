from .app import app

from fastapi import Request
from starlette.responses import RedirectResponse

from api.routers import manga, chapter, upload, user, auth, settings


app.include_router(manga.router)
app.include_router(chapter.router)
app.include_router(upload.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(settings.router)


@app.get("/", include_in_schema=False)
async def root(request: Request):
    return RedirectResponse(f"{request.scope.get('root_path')}/docs")


@app.get("/ping", tags=["Status"])
async def ping():
    """
    Ping the server
    """
    return "pong"
