from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ReelCreate(BaseModel):
    project_id: str
    file_path: str
    duration: Optional[int] = None
    format: str = "mp4"
    resolution: Optional[str] = None


class ReelResponse(BaseModel):
    id: str
    project_id: str
    file_path: str
    duration: Optional[int]
    format: str
    resolution: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ReelGenerateRequest(BaseModel):
    """Request schema for generating a reel"""
    resolution: Optional[str] = "1920x1080"
    fps: Optional[int] = 30
