import logging
from sqlalchemy.orm import Session
from typing import Optional
from app.modules.script.models import Script
from app.modules.script.schemas import ScriptUpdateRequest
from app.shared.ai.orchestrator import Orchestrator
from app.shared.prompts.script import SCRIPT_SYSTEM_PROMPT, SCRIPT_REFINE_PROMPT

logger = logging.getLogger(__name__)

class ScriptService:
    """Service for script operations"""
    
    def __init__(self, db: Session, orchestrator: Optional[Orchestrator] = None):
        self.db = db
        self.orchestrator = orchestrator or Orchestrator()
    
    def get_script(self, project_id: str) -> Optional[Script]:
        """Get script by project ID"""
        return self.db.query(Script).filter(Script.project_id == project_id).first()
    
    def create_script(self, project_id: str, content: str) -> Script:
        """Create a new script"""
        script = Script(
            project_id=project_id,
            content=content
        )
        self.db.add(script)
        self.db.commit()
        self.db.refresh(script)
        return script
    
    def update_script(self, project_id: str, update_data: ScriptUpdateRequest) -> Optional[Script]:
        """Update script content (manual edit)"""
        script = self.get_script(project_id)
        if not script:
            return None
        
        script.content = update_data.content
        self.db.commit()
        self.db.refresh(script)
        return script
    
    def approve_script(self, project_id: str) -> Optional[Script]:
        """Approve script"""
        script = self.get_script(project_id)
        if not script:
            return None
        
        script.is_approved = True
        self.db.commit()
        self.db.refresh(script)
        return script
    
    async def generate_script(self, project_id: str, project_context: dict) -> Script:
        """Generate script using AI"""
        logger.info(f"Generating script for project: {project_id}")
        
        # Build project context for AI
        context = {
            "topic": project_context.get("topic"),
            "language": project_context.get("language", "English"),
            "duration": project_context.get("duration", 60),
            "content_type": project_context.get("content_type"),
            "additional_context": project_context.get("additional_context")
        }
        logger.info(f"Project context: {context}")
        
        # Generate content
        logger.info("Calling orchestrator.generate...")
        content = await self.orchestrator.generate(
            stage="script",
            project_context=context,
            system_prompt=SCRIPT_SYSTEM_PROMPT
        )
        logger.info(f"Generated content length: {len(content)}")
        
        # Create or update script
        existing_script = self.get_script(project_id)
        if existing_script:
            logger.info("Updating existing script")
            existing_script.content = content
            existing_script.refinement_instructions = None
            self.db.commit()
            self.db.refresh(existing_script)
            return existing_script
        else:
            logger.info("Creating new script")
            return self.create_script(project_id, content)
    
    async def refine_script(self, project_id: str, instructions: str, project_context: dict) -> Optional[Script]:
        """Refine script using AI with user instructions"""
        script = self.get_script(project_id)
        if not script:
            return None
        
        # Build project context for AI
        context = {
            "topic": project_context.get("topic"),
            "language": project_context.get("language", "English"),
            "duration": project_context.get("duration", 60),
            "content_type": project_context.get("content_type"),
            "additional_context": project_context.get("additional_context")
        }
        
        # Refine content
        refined_content = await self.orchestrator.refine(
            stage="script",
            project_context=context,
            current_artifact=script.content,
            user_instructions=instructions,
            system_prompt=SCRIPT_REFINE_PROMPT
        )
        
        # Update script
        script.content = refined_content
        script.refinement_instructions = instructions
        self.db.commit()
        self.db.refresh(script)
        return script
