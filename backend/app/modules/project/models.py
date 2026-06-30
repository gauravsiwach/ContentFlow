import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    topic = Column(Text, nullable=False)
    language = Column(String(50), nullable=False, default="English")
    duration = Column(Integer, nullable=False, default=60)
    content_type = Column(String(100), nullable=False, default="Technology")
    template_id = Column(String(36), nullable=True)
    additional_context = Column(Text, nullable=True)
    status = Column(String(50), nullable=False, default="draft")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
    script = relationship("Script", back_populates="project", uselist=False, cascade="all, delete-orphan")
    scenes = relationship("Scene", back_populates="project", cascade="all, delete-orphan")
    images = relationship("Image", back_populates="project", cascade="all, delete-orphan")
    voices = relationship("Voice", back_populates="project", cascade="all, delete-orphan")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False)
    task_type = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False, default="pending")
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    project = relationship("Project", back_populates="tasks")
