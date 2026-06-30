from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ProjectCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    topic: str = Field(..., min_length=1)
    language: str = Field(default="English")
    duration: int = Field(default=60, ge=10, le=300)
    content_type: str = Field(default="Technology")
    template_id: Optional[str] = None
    additional_context: Optional[str] = None


class ProjectUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    topic: Optional[str] = Field(None, min_length=1)
    language: Optional[str] = None
    duration: Optional[int] = Field(None, ge=10, le=300)
    content_type: Optional[str] = None
    template_id: Optional[str] = None
    additional_context: Optional[str] = None
    status: Optional[str] = None


class ProjectResponse(BaseModel):
    id: str
    title: str
    topic: str
    language: str
    duration: int
    content_type: str
    template_id: Optional[str] = None
    additional_context: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProjectListResponse(BaseModel):
    projects: list[ProjectResponse]
    total: int


class ProjectStatusResponse(BaseModel):
    id: str
    status: str
    available_actions: list[str]
