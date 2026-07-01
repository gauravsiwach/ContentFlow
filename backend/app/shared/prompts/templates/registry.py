from typing import Dict, Optional
from .base import PromptTemplate
from .comedy_children import ComedyChildrenTemplate
from app.shared.content_types import ContentType


class TemplateRegistry:
    """Registry for managing content type prompt templates"""

    _templates: Dict[ContentType, PromptTemplate] = {
        ContentType.COMEDY_CHILDREN: ComedyChildrenTemplate(),
    }

    @classmethod
    def get_template(cls, content_type: ContentType) -> Optional[PromptTemplate]:
        """Get template for a specific content type"""
        return cls._templates.get(content_type)

    @classmethod
    def register_template(cls, content_type: ContentType, template: PromptTemplate) -> None:
        """Register a new template for a content type"""
        cls._templates[content_type] = template

    @classmethod
    def has_template(cls, content_type: ContentType) -> bool:
        """Check if a template exists for a content type"""
        return content_type in cls._templates
