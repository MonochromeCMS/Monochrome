import uuid

from sqlalchemy import Column, ForeignKey, delete
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from .base import Base


class UploadSession(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    manga_id = Column(UUID(as_uuid=True), ForeignKey("manga.id", ondelete="CASCADE"), nullable=False)
    manga = relationship("Manga")
    blobs = relationship("UploadedBlob", back_populates="session")

    @classmethod
    async def flush(cls, db_session: AsyncSession):
        stmt = delete(cls)
        return await db_session.execute(stmt)


class UploadedBlob(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("uploadsession.id", ondelete="CASCADE"), nullable=False)
    session = relationship("UploadSession", back_populates="blobs")
