import os
import json

from fastapi import APIRouter, Depends

from .auth import is_connected
from ..config import get_settings
from ..models.settings import Settings
from ..schemas.settings import SettingsSchema


global_settings = get_settings()
settings_path = os.path.join(global_settings.media_path, "settings.json")

router = APIRouter(prefix="/settings", tags=["Settings"])

custom_settings = Settings()


@router.get(
    "",
    response_model=SettingsSchema,
)
async def get_site_settings():
    return custom_settings.get()


@router.put("", response_model=SettingsSchema, dependencies=[Depends(is_connected)])
async def edit_site_settings(settings: SettingsSchema):
    return custom_settings.set(settings)
