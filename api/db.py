from typing import AsyncGenerator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from . import config

global_settings = config.get_settings()

engine = create_async_engine(
    global_settings.db_url,
    future=True,
    # echo=True, # To debug SQL queries
)

# expire_on_commit=False will prevent attributes from being expired
# after commit.
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


# Dependency
async def get_db() -> AsyncGenerator:
    session = async_session()
    try:
        yield session
        await session.commit()
    except SQLAlchemyError as ex:
        await session.rollback()
        raise ex
    finally:
        await session.close()
