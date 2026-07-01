from abc import ABC, abstractmethod
from typing import Dict, Any


class PromptTemplate(ABC):
    """Abstract base class for content type-specific prompt templates"""

    @abstractmethod
    def get_script_prompt(self, context: Dict[str, Any]) -> str:
        """Generate script prompt for AI generation"""
        pass

    @abstractmethod
    def get_scene_prompt(self, context: Dict[str, Any]) -> str:
        """Generate scene prompt for AI generation"""
        pass

    @abstractmethod
    def get_image_prompt(self, context: Dict[str, Any]) -> str:
        """Generate image prompt for AI generation"""
        pass

    @abstractmethod
    def get_voice_prompt(self, context: Dict[str, Any]) -> str:
        """Generate voice prompt for AI generation"""
        pass
