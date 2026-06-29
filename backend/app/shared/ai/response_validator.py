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
        import json
        import re
        import logging
        
        logger = logging.getLogger(__name__)
        
        cleaned = response.strip()
        
        # Log the raw response for debugging
        logger.info(f"Raw LLM response (first 500 chars): {cleaned[:500]}")
        logger.info(f"Raw LLM response (last 500 chars): {cleaned[-500:]}")
        
        # Minimum length check
        if len(cleaned) < 200:
            raise ValueError("Scenes response is too short (minimum 200 characters)")
        
        # Try to extract JSON from markdown code blocks or text
        json_str = cleaned
        
        # Remove markdown code blocks if present
        if "```json" in cleaned:
            match = re.search(r'```json\s*(.*?)\s*```', cleaned, re.DOTALL)
            if match:
                json_str = match.group(1).strip()
                logger.info("Extracted JSON from ```json block")
        elif "```" in cleaned:
            match = re.search(r'```\s*(.*?)\s*```', cleaned, re.DOTALL)
            if match:
                json_str = match.group(1).strip()
                logger.info("Extracted JSON from ``` block")
        
        # Try to find JSON array in the response
        if not json_str.startswith('['):
            match = re.search(r'\[.*\]', json_str, re.DOTALL)
            if match:
                json_str = match.group(0)
                logger.info("Extracted JSON array from text")
        
        logger.info(f"JSON string to parse (first 300 chars): {json_str[:300]}")
        
        # Check for valid JSON array
        try:
            scenes_data = json.loads(json_str)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON. Error: {e}")
            logger.error(f"JSON string preview: {json_str[:500]}")
            raise ValueError(f"Scenes response is not valid JSON: {e}. Response preview: {cleaned[:200]}")
        
        if not isinstance(scenes_data, list):
            raise ValueError("Scenes response must be a JSON array")
        
        if len(scenes_data) == 0:
            raise ValueError("Scenes response cannot be empty")
        
        # Validate each scene has required fields
        required_fields = ["title", "description", "duration", "voiceover_text", "image_prompt", "camera_directions", "visual_description"]
        for idx, scene in enumerate(scenes_data):
            if not isinstance(scene, dict):
                raise ValueError(f"Scene {idx} is not an object")
            
            for field in required_fields:
                if field not in scene:
                    raise ValueError(f"Scene {idx} missing required field: {field}")
                
                if not scene[field] or not str(scene[field]).strip():
                    raise ValueError(f"Scene {idx} field '{field}' is empty")
            
            # Validate duration is an integer
            if not isinstance(scene["duration"], int):
                raise ValueError(f"Scene {idx} duration must be an integer")
            
            if scene["duration"] <= 0:
                raise ValueError(f"Scene {idx} duration must be positive")
        
        return cleaned
