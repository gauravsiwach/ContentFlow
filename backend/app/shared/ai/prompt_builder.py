from typing import Optional, Dict, Any
import logging
from app.shared.content_types import ContentType
from app.shared.prompts.templates.registry import TemplateRegistry

logger = logging.getLogger(__name__)

class PromptBuilder:
    """Build prompts for AI generation"""
    
    @staticmethod
    def build(
        stage: str,
        project_context: Dict[str, Any],
        template_context: Optional[str] = None,
        current_artifact: Optional[str] = None,
        user_instructions: Optional[str] = None
    ) -> str:
        """
        Assemble prompt string for AI generation
        
        Args:
            stage: Current workflow stage (e.g., 'script', 'scenes')
            project_context: Project information (topic, language, duration, content_type, etc.)
            template_context: Optional template context
            current_artifact: Current artifact content (for refinement)
            user_instructions: User instructions for refinement
        
        Returns:
            Assembled prompt string
        """
        content_type_str = project_context.get('content_type', 'comedy_children')
        
        logger.info(f"Building prompt for stage: {stage}, content_type: {content_type_str}")
        
        # Try to use template system if available
        try:
            content_type = ContentType(content_type_str)
            template = TemplateRegistry.get_template(content_type)
            
            if template:
                logger.info(f"Using specialized template for content_type: {content_type_str}")
                return PromptBuilder._build_with_template(
                    template, stage, project_context, 
                    template_context, current_artifact, user_instructions
                )
            else:
                logger.warning(f"No template found for content_type: {content_type_str}, using default")
        except (ValueError, Exception) as e:
            logger.warning(f"Invalid content_type: {content_type_str}, error: {e}, using default")
            # Fall back to default if content type is invalid or template not found
            pass
        
        # Default prompt building (legacy behavior)
        logger.info(f"Using default prompt building for stage: {stage}")
        return PromptBuilder._build_default(
            stage, project_context, template_context, 
            current_artifact, user_instructions
        )
    
    @staticmethod
    def _build_with_template(
        template,
        stage: str,
        project_context: Dict[str, Any],
        template_context: Optional[str] = None,
        current_artifact: Optional[str] = None,
        user_instructions: Optional[str] = None
    ) -> str:
        """Build prompt using content type template"""
        prompt_parts = []
        
        # Get specialized prompt from template based on stage
        if stage == 'script':
            prompt_parts.append(template.get_script_prompt(project_context))
        elif stage == 'scenes':
            prompt_parts.append(template.get_scene_prompt(project_context))
        elif stage == 'image':
            prompt_parts.append(template.get_image_prompt(project_context))
        elif stage == 'voice':
            prompt_parts.append(template.get_voice_prompt(project_context))
        else:
            # Fall back to default for unknown stages
            return PromptBuilder._build_default(
                stage, project_context, template_context,
                current_artifact, user_instructions
            )
        
        # Add current artifact if present (for refinement)
        if current_artifact:
            prompt_parts.append(f"\n\nCurrent Content:\n{current_artifact}")
        
        # Add user instructions if present
        if user_instructions:
            prompt_parts.append(f"\n\nInstructions: {user_instructions}")
        
        return "\n".join(prompt_parts)
    
    @staticmethod
    def _build_default(
        stage: str,
        project_context: Dict[str, Any],
        template_context: Optional[str] = None,
        current_artifact: Optional[str] = None,
        user_instructions: Optional[str] = None
    ) -> str:
        """Build prompt using default legacy approach"""
        prompt_parts = []
        
        # Add project context
        if project_context.get('topic'):
            prompt_parts.append(f"Topic: {project_context.get('topic', '')}")
        prompt_parts.append(f"Language: {project_context.get('language', 'English')}")
        prompt_parts.append(f"Duration: {project_context.get('duration', 60)} seconds")
        if project_context.get('content_type'):
            prompt_parts.append(f"Content Type: {project_context.get('content_type', '')}")
        
        # Add script content for scene generation
        if project_context.get('script'):
            prompt_parts.append(f"\nScript:\n{project_context['script']}")
        
        if project_context.get('additional_context'):
            prompt_parts.append(f"Additional Context: {project_context['additional_context']}")
        
        # Add current artifact if present (for refinement)
        if current_artifact:
            prompt_parts.append(f"\nCurrent Content:\n{current_artifact}")
        
        # Add user instructions if present
        if user_instructions:
            prompt_parts.append(f"\nInstructions: {user_instructions}")
        
        # Add template context if present
        if template_context:
            prompt_parts.append(f"\n{template_context}")
        
        return "\n".join(prompt_parts)
