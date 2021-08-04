import uuid

from sqlalchemy import Column, ForeignKey, delete, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from .base import Base


class UploadSession(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chapter_id = Column(UUID(as_uuid=True), ForeignKey("chapter.id", ondelete="CASCADE"))
    manga_id = Column(UUID(as_uuid=True), ForeignKey("manga.id", ondelete="CASCADE"), nullable=False)
    manga = relationship("Manga", back_populates="sessions")
    chapter = relationship("Chapter", back_populates="sessions")
    blobs = relationship("UploadedBlob", back_populates="session", cascade="all, delete", passive_deletes=True)

    @classmethod
    async def flush(cls, db_session: AsyncSession):
        stmt = delete(cls)
        return await db_session.execute(stmt)


class UploadedBlob(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    session_id = Column(UUID(as_uuid=True), ForeignKey("uploadsession.id", ondelete="CASCADE"), nullable=False)
    session = relationship("UploadSession", back_populates="blobs")
