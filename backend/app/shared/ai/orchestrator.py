import logging
from typing import Dict, Any, Optional
from app.config import settings
from .ollama_client import OllamaClient
from .prompt_builder import PromptBuilder
from .response_validator import ResponseValidator

logger = logging.getLogger(__name__)

class Orchestrator:
    """Orchestrate AI generation and refinement operations"""
    
    def __init__(self, ollama_client: Optional[OllamaClient] = None):
        self.client = ollama_client or OllamaClient()
        self.prompt_builder = PromptBuilder()
        self.validator = ResponseValidator()
    
    async def generate(
        self,
        stage: str,
        project_context: Dict[str, Any],
        system_prompt: str,
        model: Optional[str] = None
    ) -> str:
        """
        Generate content using AI
        
        Args:
            stage: Current workflow stage
            project_context: Project information
            system_prompt: System prompt for the AI
            model: Model to use (from env OLLAMA_MODEL if not provided)
        
        Returns:
            Generated and validated content
        
        Raises:
            ValueError: If validation fails
            httpx.HTTPError: If API call fails
        """
        logger.info(f"Orchestrator.generate called for stage: {stage}")
        logger.info(f"Using model: {model or settings.OLLAMA_MODEL}")
        
        # Build prompt
        logger.info("Building prompt...")
        prompt = self.prompt_builder.build(
            stage=stage,
            project_context=project_context
        )
        logger.info(f"Prompt length: {len(prompt)}")
        
        # Generate content
        logger.info("Calling Ollama client.generate...")
        response = await self.client.generate(
            prompt=prompt,
            model=model or settings.OLLAMA_MODEL,
            system_prompt=system_prompt
        )
        logger.info(f"Ollama response length: {len(response)}")
        
        # Validate response
        logger.info("Validating response...")
        validated_content = self.validator.validate(response, stage)
        
        logger.info(f"Successfully generated content for stage: {stage}")
        return validated_content
    
    async def refine(
        self,
        stage: str,
        project_context: Dict[str, Any],
        current_artifact: str,
        user_instructions: str,
        system_prompt: str,
        model: Optional[str] = None
    ) -> str:
        """
        Refine existing content using AI with user instructions
        
        Args:
            stage: Current workflow stage
            project_context: Project information
            current_artifact: Current content to refine
            user_instructions: User feedback/instructions
            system_prompt: System prompt for the AI
            model: Model to use (from env OLLAMA_MODEL if not provided)
        
        Returns:
            Refined and validated content
        
        Raises:
            ValueError: If validation fails
            httpx.HTTPError: If API call fails
        """
        # Build refinement prompt
        prompt = self.prompt_builder.build(
            stage=stage,
            project_context=project_context,
            current_artifact=current_artifact,
            user_instructions=user_instructions
        )
        
        # Generate refined content
        response = await self.client.generate(
            prompt=prompt,
            model=model or settings.OLLAMA_MODEL,
            system_prompt=system_prompt
        )
        
        # Validate response
        validated_content = self.validator.validate(response, stage)
        
        logger.info(f"Successfully refined content for stage: {stage}")
        return validated_content
