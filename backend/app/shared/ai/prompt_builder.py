from typing import Optional, Dict, Any

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
        prompt_parts = []
        
        # Add project context
        prompt_parts.append(f"Topic: {project_context.get('topic', '')}")
        prompt_parts.append(f"Language: {project_context.get('language', 'English')}")
        prompt_parts.append(f"Duration: {project_context.get('duration', 60)} seconds")
        prompt_parts.append(f"Content Type: {project_context.get('content_type', '')}")
        
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
