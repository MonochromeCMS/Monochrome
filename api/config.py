import logging
import os
from functools import lru_cache

from pydantic import BaseSettings

log = logging.getLogger(__name__)


class Settings(BaseSettings):
    """
    BaseSettings, from Pydantic, validates the data so that when we create an instance of Settings,
     environment and testing will have types of str and bool, respectively.
    Parameters:
    pg_user (str):
    pg_pass (str):
    pg_database: (str):
    asyncpg_url: AnyUrl:
    asyncpg_test_url: AnyUrl:
    Returns:
    instance of Settings
    """

    db_url: str = os.getenv("DB_URL", "")

    jwt_secret_key: str = os.getenv("SECRET_KEY", "")
    jwt_algorithm: str = os.getenv("ALGORITHM", "HS256")
    jwt_access_toke_expire_minutes: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)

    media_path: str = os.getenv("MEDIA_PATH", "/media")


@lru_cache()
def get_settings():
    log.info("Loading config settings from the environment...")
    return Settings()
