import logging
import json
from sqlalchemy.orm import Session
from typing import Optional, List
from app.modules.scene.models import Scene
from app.modules.scene.schemas import SceneCreate, SceneUpdate
from app.shared.ai.orchestrator import Orchestrator
from app.shared.prompts.scene import SCENE_SYSTEM_PROMPT, SCENE_REFINE_PROMPT

logger = logging.getLogger(__name__)


class SceneService:
    """Service for scene operations"""
    
    def __init__(self, db: Session, orchestrator: Optional[Orchestrator] = None):
        self.db = db
        self.orchestrator = orchestrator or Orchestrator()
    
    def get_scenes(self, project_id: str) -> List[Scene]:
        """Get all scenes for a project"""
        logger.info(f"get_scenes called with project_id: {project_id}, type: {type(project_id)}")
        return self.db.query(Scene).filter(Scene.project_id == project_id).order_by(Scene.scene_number).all()
    
    def create_scene(self, scene_data: SceneCreate) -> Scene:
        """Create a single scene"""
        scene = Scene(
            project_id=scene_data.project_id,
            scene_number=scene_data.scene_number,
            title=scene_data.title,
            description=scene_data.description,
            duration=scene_data.duration,
            voiceover_text=scene_data.voiceover_text,
            image_prompt=scene_data.image_prompt,
            camera_directions=scene_data.camera_directions,
            visual_description=scene_data.visual_description
        )
        self.db.add(scene)
        self.db.commit()
        self.db.refresh(scene)
        return scene
    
    def update_scene(self, scene_id: str, update_data: SceneUpdate) -> Optional[Scene]:
        """Update a single scene"""
        scene = self.db.query(Scene).filter(Scene.id == scene_id).first()
        if not scene:
            return None
        
        if update_data.title is not None:
            scene.title = update_data.title
        if update_data.description is not None:
            scene.description = update_data.description
        if update_data.duration is not None:
            scene.duration = update_data.duration
        if update_data.voiceover_text is not None:
            scene.voiceover_text = update_data.voiceover_text
        if update_data.image_prompt is not None:
            scene.image_prompt = update_data.image_prompt
        if update_data.camera_directions is not None:
            scene.camera_directions = update_data.camera_directions
        if update_data.visual_description is not None:
            scene.visual_description = update_data.visual_description
        
        self.db.commit()
        self.db.refresh(scene)
        return scene
    
    def approve_scenes(self, project_id: str) -> List[Scene]:
        """Approve all scenes for a project"""
        scenes = self.get_scenes(project_id)
        for scene in scenes:
            scene.is_approved = True
        self.db.commit()
        for scene in scenes:
            self.db.refresh(scene)
        return scenes
    
    def delete_scenes(self, project_id: str) -> bool:
        """Delete all scenes for a project"""
        logger.info(f"delete_scenes called with project_id: {project_id}, type: {type(project_id)}")
        scenes = self.get_scenes(project_id)
        for scene in scenes:
            self.db.delete(scene)
        self.db.commit()
        return True
    
    async def generate_scenes(self, project_id: str, project_context: dict, script_content: str, user_instructions: Optional[str] = None) -> List[Scene]:
        """Generate scenes using AI"""
        logger.info(f"Generating scenes for project: {project_id}")
        
        # Build context for AI
        context = {
            "script": script_content,
            "duration": project_context.get("duration", 60),
            "content_type": project_context.get("content_type"),
            "language": project_context.get("language", "English"),
            "user_instructions": user_instructions
        }
        logger.info(f"Scene generation context: {context}")
        
        # Generate scenes
        logger.info("Calling orchestrator.generate for scenes...")
        response = await self.orchestrator.generate(
            stage="scenes",
            project_context=context,
            system_prompt=SCENE_SYSTEM_PROMPT
        )
        logger.info(f"Generated scenes response length: {len(response)}")
        
        # Parse JSON response
        try:
            scenes_data = json.loads(response)
            if not isinstance(scenes_data, list):
                raise ValueError("Response is not a JSON array")
            logger.info(f"Parsed {len(scenes_data)} scenes from AI response")
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse scenes JSON: {e}")
            raise ValueError(f"Invalid JSON response from AI: {e}")
        
        # Delete existing scenes for this project
        logger.info(f"About to delete scenes for project_id: {project_id}, type: {type(project_id)}")
        self.delete_scenes(project_id)
        
        # Create new scenes
        created_scenes = []
        for idx, scene_data in enumerate(scenes_data):
            scene_create = SceneCreate(
                project_id=project_id,
                scene_number=idx + 1,
                title=scene_data.get("title", ""),
                description=scene_data.get("description", ""),
                duration=scene_data.get("duration", 10),
                voiceover_text=scene_data.get("voiceover_text", ""),
                image_prompt=scene_data.get("image_prompt", ""),
                camera_directions=scene_data.get("camera_directions", ""),
                visual_description=scene_data.get("visual_description", "")
            )
            scene = self.create_scene(scene_create)
            created_scenes.append(scene)
        
        logger.info(f"Created {len(created_scenes)} scenes for project {project_id}")
        return created_scenes
    
    async def refine_scenes(self, project_id: str, instructions: str, project_context: dict) -> List[Scene]:
        """Refine scenes using AI with user instructions"""
        logger.info(f"Refining scenes for project: {project_id}")
        
        scenes = self.get_scenes(project_id)
        if not scenes:
            logger.warning(f"No scenes found for project {project_id}")
            return []
        
        # Build current scenes context for AI
        scenes_context = [
            {
                "title": scene.title,
                "description": scene.description,
                "duration": scene.duration,
                "voiceover_text": scene.voiceover_text,
                "image_prompt": scene.image_prompt,
                "camera_directions": scene.camera_directions,
                "visual_description": scene.visual_description
            }
            for scene in scenes
        ]
        
        context = {
            "current_scenes": scenes_context,
            "duration": project_context.get("duration", 60),
            "content_type": project_context.get("content_type"),
            "language": project_context.get("language", "English"),
            "user_instructions": instructions
        }
        
        # Refine scenes
        logger.info("Calling orchestrator.refine for scenes...")
        response = await self.orchestrator.refine(
            stage="scenes",
            project_context=context,
            current_artifact=json.dumps(scenes_context),
            user_instructions=instructions,
            system_prompt=SCENE_REFINE_PROMPT
        )
        
        # Parse JSON response
        try:
            scenes_data = json.loads(response)
            if not isinstance(scenes_data, list):
                raise ValueError("Response is not a JSON array")
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse refined scenes JSON: {e}")
            raise ValueError(f"Invalid JSON response from AI: {e}")
        
        # Delete existing scenes and create new ones
        self.delete_scenes(project_id)
        
        # Create refined scenes
        created_scenes = []
        for idx, scene_data in enumerate(scenes_data):
            scene_create = SceneCreate(
                project_id=project_id,
                scene_number=idx + 1,
                title=scene_data.get("title", ""),
                description=scene_data.get("description", ""),
                duration=scene_data.get("duration", 10),
                voiceover_text=scene_data.get("voiceover_text", ""),
                image_prompt=scene_data.get("image_prompt", ""),
                camera_directions=scene_data.get("camera_directions", ""),
                visual_description=scene_data.get("visual_description", "")
            )
            scene = self.create_scene(scene_create)
            created_scenes.append(scene)
        
        logger.info(f"Refined and created {len(created_scenes)} scenes for project {project_id}")
        return created_scenes
