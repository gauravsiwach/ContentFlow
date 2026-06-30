from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import uuid
from datetime import datetime


class Voice(Base):
    __tablename__ = "voices"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    scene_id = Column(String(36), ForeignKey("scenes.id"), nullable=False)
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False)
    file_path = Column(String(512), nullable=False)
    voice_used = Column(String(100), nullable=False)  # e.g., "ऋतिका" for Hindi
    text_used = Column(String(2000), nullable=False)  # The script text that was converted
    duration = Column(String(50), nullable=True)  # Audio duration in seconds
    is_approved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    scene = relationship("Scene", back_populates="voices")
    project = relationship("Project", back_populates="voices")
