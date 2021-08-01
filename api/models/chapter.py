import uuid

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from .base import Base


class Chapter(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    volume = Column(Integer, nullable=True)
    number = Column(Integer, nullable=False)
    length = Column(Integer, nullable=False)
    manga_id = Column(UUID(as_uuid=True), ForeignKey('manga.id', ondelete="CASCADE"), nullable=False)
    manga = relationship("Manga", back_populates="chapters")
