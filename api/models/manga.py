import uuid
import enum

from sqlalchemy import Column, String, select, Numeric, Enum, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from .base import Base
from ..exceptions import NotFoundHTTPException


class Status(str, enum.Enum):
    ongoing = "ongoing"
    completed = "completed"
    hiatus = "hiatus"
    cancelled = "cancelled"


class Manga(Base):
    __tablename__ = "manga"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    author = Column(String, nullable=False)
    artist = Column(String, nullable=False)
    year = Column(Numeric(4, 0))
    status = Column(Enum(Status), nullable=False)
    version = Column(Integer, default=1)

    @classmethod
    async def find(cls, db_session: AsyncSession, _id: uuid.UUID):
        stmt = select(cls).where(cls.id == _id)
        result = await db_session.execute(stmt)
        instance = result.scalars().first()
        if instance is None:
            raise NotFoundHTTPException()
        else:
            return instance

    @classmethod
    async def search(cls, db_session: AsyncSession, title: str, limit: int = 20, offset: int = 0):
        escaped_title = title.replace("%", "\\%")
        stmt = select(cls).where(cls.title.ilike(f"%{escaped_title}%"))
        return await cls.pagination(db_session, stmt, limit, offset)
