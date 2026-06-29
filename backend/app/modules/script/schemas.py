from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ScriptResponse(BaseModel):
    """Response model for script"""
    id: str
    project_id: str
    content: str
    refinement_instructions: Optional[str] = None
    is_approved: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ScriptGenerateRequest(BaseModel):
    """Request model for script generation"""
    pass  # No additional fields needed, uses project context


class ScriptRefineRequest(BaseModel):
    """Request model for script refinement"""
    instructions: str


class ScriptUpdateRequest(BaseModel):
    """Request model for manual script update"""
    content: str


class ScriptApproveRequest(BaseModel):
    """Request model for script approval"""
    pass  # No additional fields needed


class TaskResponse(BaseModel):
    """Response model for background task"""
    id: str
    project_id: str
    task_type: str
    status: str
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
