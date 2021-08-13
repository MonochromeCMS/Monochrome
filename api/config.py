import logging
from functools import lru_cache

from pydantic import BaseSettings, AnyUrl, Field

log = logging.getLogger(__name__)


class Settings(BaseSettings):
    db_url: AnyUrl

    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_access_toke_expire_minutes: int = 60

    media_path: str = "/media"

    max_page_limit: int = Field(50, gt=0)


@lru_cache()
def get_settings():
    log.info("Loading config settings from the environment...")
    return Settings()
