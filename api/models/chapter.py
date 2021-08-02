import uuid

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, func, select
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import UUID

from .base import Base


class Chapter(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    volume = Column(Integer, nullable=True)
    number = Column(String, nullable=False)
    length = Column(Integer, nullable=False)
    upload_time = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    manga_id = Column(UUID(as_uuid=True), ForeignKey("manga.id", ondelete="CASCADE"), nullable=False)
    manga = relationship("Manga", back_populates="chapters")

    __mapper_args__ = {"eager_defaults": True}

    @classmethod
    async def latest(cls, db_session: AsyncSession, limit: int = 20, offset: int = 0):
        return await cls.pagination(db_session, select(cls), limit, offset, (cls.upload_time.desc(),))

    @classmethod
    async def from_manga(cls, db_session: AsyncSession, manga_id: uuid.UUID):
        stmt = select(cls).where(cls.manga_id == manga_id).order_by(cls.number.desc())
        result = await db_session.execute(stmt)
        return result.scalars().all()
