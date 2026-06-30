from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import uuid
from datetime import datetime


class Reel(Base):
    __tablename__ = "reels"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    file_path = Column(String(512), nullable=False)
    duration = Column(Integer, nullable=True)  # Duration in seconds
    format = Column(String(50), default="mp4")
    resolution = Column(String(50), nullable=True)  # e.g., "1920x1080"
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    project = relationship("Project", back_populates="reel")
