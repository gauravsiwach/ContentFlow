import logging

logger = logging.getLogger(__name__)

class ResponseValidator:
    """Validate AI responses"""
    
    @staticmethod
    def validate(response: str, stage: str) -> str:
        """
        Validate AI response based on stage
        
        Args:
            response: The AI response to validate
            stage: Current workflow stage (e.g., 'script', 'scenes')
        
        Returns:
            Validated response content
        
        Raises:
            ValueError: If validation fails
        """
        if not response or not response.strip():
            raise ValueError(f"Response is empty for stage: {stage}")
        
        # Stage-specific validation
        if stage == "script":
            return ResponseValidator._validate_script(response)
        elif stage == "scenes":
            return ResponseValidator._validate_scenes(response)
        else:
            # Default validation: just check non-empty
            return response.strip()
    
    @staticmethod
    def _validate_script(response: str) -> str:
        """Validate script response"""
        cleaned = response.strip()
        
        # Minimum length check (100 characters)
        if len(cleaned) < 100:
            raise ValueError("Script response is too short (minimum 100 characters)")
        
        # Check for actual content (not just repeated phrases)
        if len(set(cleaned.split())) < 20:
            raise ValueError("Script response lacks sufficient content diversity")
        
        # Check for production elements that should NOT be in script
        production_patterns = [
            r'\[.*?\]',  # Anything in brackets [like this] - visual/camera directions
            r'Scene \d+',  # Scene headings like "Scene 1"
            r'Intro:',  # Scene section headings
            r'Scene \d+:',
            r'Outro:',
            r'Camera.*:',  # Camera directions
            r'Cut to',  # Camera directions
            r'Zoom',  # Camera directions
            r'Pan',  # Camera directions
            r'Music:',  # Music instructions
            r'Sound:',  # Sound instructions
            r'Audio:',  # Audio instructions
            r'Text overlay:',  # Text overlays
            r'Word count:',  # Meta annotations
            r'Speaking pace:',  # Meta annotations
            r'Approximate',  # Meta annotations
        ]
        
        import re
        for pattern in production_patterns:
            if re.search(pattern, cleaned, re.IGNORECASE):
                raise ValueError(f"Script contains production elements (pattern: {pattern}). Script should contain ONLY spoken narration.")
        
        return cleaned
    
    @staticmethod
    def _validate_scenes(response: str) -> str:
        """Validate scenes response"""
        cleaned = response.strip()
        
        # Minimum length check
        if len(cleaned) < 200:
            raise ValueError("Scenes response is too short (minimum 200 characters)")
        
        return cleaned
