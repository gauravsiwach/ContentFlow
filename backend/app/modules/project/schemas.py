from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional
from app.shared.content_types import ContentType, ContentTypeConfig


class ProjectCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    topic: str = Field(..., min_length=1)
    language: str = Field(default="English")
    duration: int = Field(default=60, ge=10, le=300)
    content_type: str = Field(default=ContentType.COMEDY_CHILDREN.value)
    template_id: Optional[str] = None
    additional_context: Optional[str] = None

    @field_validator('content_type')
    @classmethod
    def validate_content_type(cls, v):
        if not ContentTypeConfig.is_valid_content_type(v):
            raise ValueError(f"Invalid content_type. Must be one of: {[ct.value for ct in ContentTypeConfig.get_all_content_types()]}")
        return v


class ProjectUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    topic: Optional[str] = Field(None, min_length=1)
    language: Optional[str] = None
    duration: Optional[int] = Field(None, ge=10, le=300)
    content_type: Optional[str] = None
    template_id: Optional[str] = None
    additional_context: Optional[str] = None
    status: Optional[str] = None

    @field_validator('content_type')
    @classmethod
    def validate_content_type(cls, v):
        if v is not None and not ContentTypeConfig.is_valid_content_type(v):
            raise ValueError(f"Invalid content_type. Must be one of: {[ct.value for ct in ContentTypeConfig.get_all_content_types()]}")
        return v


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
