import os
import json

from ..config import get_settings
from ..schemas.settings import SettingsSchema


global_settings = get_settings()
settings_path = os.path.join(global_settings.media_path, "settings.json")


class Settings:
    custom_settings = None

    def __init__(self):
        try:
            file = open(settings_path, "r", encoding="utf8")
            self.custom_settings = SettingsSchema(**json.load(file))
        except FileNotFoundError:
            self.custom_settings = SettingsSchema()

    def get(self):
        return self.custom_settings

    def set(self, settings: SettingsSchema) -> SettingsSchema:
        with open(settings_path, "w", encoding="utf8") as file:
            json.dump(settings.dict(), file)
        self.custom_settings = settings
        return settings
