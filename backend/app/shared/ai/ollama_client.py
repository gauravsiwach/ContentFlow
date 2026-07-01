import httpx
import logging
from typing import Optional, Dict, Any
from app.config import settings

logger = logging.getLogger(__name__)

class OllamaClient:
    """HTTP client for Ollama API"""
    
    def __init__(self, base_url: Optional[str] = None, timeout: Optional[int] = None):
        self.base_url = base_url or settings.OLLAMA_BASE_URL
        self.timeout = timeout or settings.OLLAMA_TIMEOUT
    
    async def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7
    ) -> str:
        """
        Generate text using Ollama API
        
        Args:
            prompt: The user prompt
            model: The model to use (from env OLLAMA_MODEL)
            system_prompt: Optional system prompt
            temperature: Sampling temperature (0.0-1.0)
        
        Returns:
            Generated text response
        
        Raises:
            httpx.HTTPError: If the request fails
        """
        logger.info(f"OllamaClient.generate called with base_url: {self.base_url}")
        url = f"{self.base_url}/api/generate"
        
        model_name = model or settings.OLLAMA_MODEL
        logger.info(f"Using model: {model_name}")
        
        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
            }
        }
        
        if system_prompt:
            payload["system"] = system_prompt
        
        logger.info(f"Sending request to Ollama at {url}")
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                logger.info("HTTP client created, sending POST request...")
                response = await client.post(url, json=payload)
                logger.info(f"Response status code: {response.status_code}")
                response.raise_for_status()
                data = response.json()
                # logger.info(f"Full raw response from Ollama API: {data}")
                result = data.get("response", "")
                logger.info(f"Ollama response received, length: {len(result)}")
                return result
        except httpx.HTTPError as e:
            logger.error(f"Ollama API error: {e}", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"Unexpected error calling Ollama: {e}", exc_info=True)
            raise
    
    async def check_connection(self) -> bool:
        """
        Check if Ollama is running and accessible
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            url = f"{self.base_url}/api/tags"
            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.get(url)
                response.raise_for_status()
                return True
        except Exception as e:
            logger.warning(f"Ollama connection check failed: {e}")
            return False
