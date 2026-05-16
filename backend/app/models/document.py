from sqlalchemy import Column, String, Integer, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base, TimestampMixin
import uuid

class Document(Base, TimestampMixin):
    __tablename__ = "documents"

    user_id        = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    filename       = Column(String, nullable=False)
    original_name  = Column(String, nullable=False)
    file_type      = Column(String, nullable=False)
    file_size      = Column(Integer, nullable=False)
    content        = Column(Text, nullable=True)
    summary        = Column(Text, nullable=True)
    status         = Column(String, default="processing")
    vector_id      = Column(String, nullable=True)