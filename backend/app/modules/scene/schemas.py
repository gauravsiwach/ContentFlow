from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class SceneBase(BaseModel):
    title: str
    description: str
    duration: int
    voiceover_text: str
    image_prompt: str
    camera_directions: str
    visual_description: str


class SceneCreate(SceneBase):
    project_id: str
    scene_number: int


class SceneUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    duration: Optional[int] = None
    voiceover_text: Optional[str] = None
    image_prompt: Optional[str] = None
    camera_directions: Optional[str] = None
    visual_description: Optional[str] = None


class SceneResponse(SceneBase):
    id: str
    project_id: str
    scene_number: int
    is_approved: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SceneListResponse(BaseModel):
    scenes: List[SceneResponse]
    total_count: int
    total_duration: int


class SceneGenerateRequest(BaseModel):
    user_instructions: Optional[str] = None


class SceneRefineRequest(BaseModel):
    user_instructions: str
