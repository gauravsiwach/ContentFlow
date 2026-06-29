from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class ImageCreate(BaseModel):
    scene_id: str
    project_id: str
    file_path: str
    prompt_used: str


class ImageUpdate(BaseModel):
    file_path: Optional[str] = None
    prompt_used: Optional[str] = None
    is_approved: Optional[bool] = None


class ImageResponse(BaseModel):
    id: str
    scene_id: str
    project_id: str
    file_path: str
    prompt_used: str
    is_approved: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ImageListResponse(BaseModel):
    images: List[ImageResponse]
    total_count: int


class ImageGenerateRequest(BaseModel):
    user_instructions: Optional[str] = None


class ImageRefineRequest(BaseModel):
    image_id: str
    new_prompt: str
