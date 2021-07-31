from .app import app

from starlette.responses import RedirectResponse


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse("/docs")


@app.get("/ping")
async def ping():
    return "pong"
