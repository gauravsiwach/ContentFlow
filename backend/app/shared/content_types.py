from enum import Enum
from typing import Dict, List, Optional


class ContentType(str, Enum):
    """Content type enum for project categorization"""
    COMEDY_CHILDREN = "comedy_children"
    # Future content types can be added here
    # EDUCATIONAL = "educational"
    # MARKETING = "marketing"


class ContentTypeConfig:
    """Configuration for content types with metadata"""

    CONFIGS: Dict[ContentType, Dict] = {
        ContentType.COMEDY_CHILDREN: {
            "display_name": "Comedy (Children)",
            "description": "Humorous content designed for children with simple language, relatable situations, and positive messages",
            "target_audience": "Children",
            "age_range": "5-10 years",
            "language_complexity": "simple",
            "visual_style": "cartoon",
            "voice_style": "energetic_playful",
            "scene_duration": "3-8 seconds",
            "humor_style": "slapstick, physical comedy, wordplay",
            "content_guidelines": [
                "Age-appropriate humor",
                "Simple vocabulary",
                "Short attention span pacing",
                "Physical comedy and visual humor",
                "Positive, uplifting messages",
                "Relatable everyday situations"
            ]
        }
    }

    @classmethod
    def get_config(cls, content_type: ContentType) -> Dict:
        """Get configuration for a content type"""
        return cls.CONFIGS.get(content_type, {})

    @classmethod
    def get_display_name(cls, content_type: ContentType) -> str:
        """Get display name for a content type"""
        return cls.CONFIGS.get(content_type, {}).get("display_name", content_type.value)

    @classmethod
    def get_all_content_types(cls) -> List[ContentType]:
        """Get all available content types"""
        return list(cls.CONFIGS.keys())

    @classmethod
    def is_valid_content_type(cls, content_type: str) -> bool:
        """Check if a content type string is valid"""
        try:
            ContentType(content_type)
            return content_type in cls.CONFIGS
        except ValueError:
            return False
