from .app import app
from .config import get_settings

from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from api.routers import manga, chapter, upload, user, auth, settings, autocomplete

global_settings = get_settings()

app.include_router(manga.router)
app.include_router(chapter.router)
app.include_router(upload.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(settings.router)
app.include_router(autocomplete.router)


origins = global_settings.cors_origins.split(',')

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
async def root(request: Request):
    return RedirectResponse(f"{request.scope.get('root_path')}/docs", status_code=301)


@app.get("/ping", tags=["Status"])
async def ping():
    """
    Ping the server
    """
    return "pong"
