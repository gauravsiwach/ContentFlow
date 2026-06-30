import logging
from typing import Optional
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

# Valid state transitions
VALID_TRANSITIONS = {
    "draft": ["script_generated"],
    "script_generated": ["script_approved"],
    "script_approved": ["scenes_generated"],
    "scenes_generated": ["scenes_approved"],
    "scenes_approved": ["images_generated"],
    "images_generated": ["images_approved"],
    "images_approved": ["voices_generated"],
    "voices_generated": ["voices_approved"],
    "voices_approved": ["reel_generated"],
    "reel_generated": ["completed"],
    "completed": []
}

class WorkflowService:
    """Service for managing workflow state transitions"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def validate_state(self, project_id: str, current_status: str, target_status: str) -> bool:
        """
        Validate if a state transition is allowed
        
        Args:
            project_id: Project ID
            current_status: Current project status
            target_status: Target status to transition to
        
        Returns:
            True if transition is valid, False otherwise
        """
        valid_next_states = VALID_TRANSITIONS.get(current_status, [])
        return target_status in valid_next_states
    
    def can_generate_script(self, project_id: str, current_status: str) -> bool:
        """
        Check if script generation is allowed for the project

        Args:
            project_id: Project ID
            current_status: Current project status

        Returns:
            True if script generation is allowed, False otherwise
        """
        return current_status == "draft"

    def can_generate_scenes(self, project_id: str) -> bool:
        """
        Check if scene generation is allowed for the project

        Args:
            project_id: Project ID

        Returns:
            True if scene generation is allowed, False otherwise
        """
        from app.modules.project import service as project_service
        project = project_service.get_project(self.db, project_id)
        return project.status == "script_approved" if project else False

    def can_generate_images(self, project_id: str) -> bool:
        """
        Check if image generation is allowed for the project

        Args:
            project_id: Project ID

        Returns:
            True if image generation is allowed, False otherwise
        """
        from app.modules.project import service as project_service
        project = project_service.get_project(self.db, project_id)
        return project.status == "scenes_approved" if project else False

    def can_approve_images(self, project_id: str) -> bool:
        """
        Check if image approval is allowed for the project

        Args:
            project_id: Project ID

        Returns:
            True if image approval is allowed, False otherwise
        """
        from app.modules.project import service as project_service
        project = project_service.get_project(self.db, project_id)
        return project.status == "images_generated" if project else False

    def can_generate_voices(self, project_id: str) -> bool:
        """
        Check if voice generation is allowed for the project

        Args:
            project_id: Project ID

        Returns:
            True if voice generation is allowed, False otherwise
        """
        from app.modules.project import service as project_service
        project = project_service.get_project(self.db, project_id)
        return project.status == "images_approved" if project else False
    
    def advance_state(self, project_id: str, current_status: str, target_status: str) -> bool:
        """
        Advance project state if transition is valid
        
        Args:
            project_id: Project ID
            current_status: Current project status
            target_status: Target status to transition to
        
        Returns:
            True if state advanced, False if transition invalid
        """
        if not self.validate_state(project_id, current_status, target_status):
            logger.warning(
                f"Invalid state transition for project {project_id}: "
                f"{current_status} -> {target_status}"
            )
            return False
        
        logger.info(f"Advancing project {project_id} from {current_status} to {target_status}")
        return True
    
    def get_current_stage(self, current_status: str) -> str:
        """
        Get the current workflow stage based on status
        
        Args:
            current_status: Current project status
        
        Returns:
            Current stage name
        """
        if current_status in ["draft", "script_generated", "script_approved"]:
            return "script"
        elif current_status in ["scenes_generated", "scenes_approved"]:
            return "scenes"
        elif current_status in ["images_generated", "images_approved"]:
            return "images"
        elif current_status in ["voice_generated", "voice_approved"]:
            return "voice"
        elif current_status in ["reel_generated", "completed"]:
            return "reel"
        else:
            return "unknown"
