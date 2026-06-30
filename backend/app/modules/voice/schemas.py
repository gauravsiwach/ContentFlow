from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class VoiceCreate(BaseModel):
    scene_id: str
    project_id: str
    file_path: str
    voice_used: str
    text_used: str
    duration: Optional[str] = None


class VoiceResponse(BaseModel):
    id: str
    scene_id: str
    project_id: str
    file_path: str
    voice_used: str
    text_used: str
    duration: Optional[str]
    is_approved: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class VoiceGenerateRequest(BaseModel):
    user_instructions: Optional[str] = None


class VoiceRefineRequest(BaseModel):
    new_text: str


class VoiceListResponse(BaseModel):
    voices: list[VoiceResponse]
    total_count: int
