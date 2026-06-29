import httpx
import base64
import logging
from typing import Optional
from app.config import settings

logger = logging.getLogger(__name__)


class OllamaImageClient:
    """Client for Ollama image generation API"""

    def __init__(self, base_url: Optional[str] = None, model: Optional[str] = None):
        self.base_url = base_url or settings.OLLAMA_BASE_URL
        self.model = model or settings.OLLAMA_IMAGE_MODEL
        self.timeout = 300  # 5 minutes default

    async def generate(self, prompt: str, size: str = "1024x1024") -> bytes:
        """
        Generate an image from text prompt using Ollama

        Args:
            prompt: Text description of the image
            size: Image dimensions (e.g., "1024x1024")

        Returns:
            Image data as bytes

        Raises:
            Exception: If image generation fails
        """
        url = f"{self.base_url}/v1/images/generations"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "size": size,
            "n": 1,
            "response_format": "b64_json"
        }

        logger.info(f"Generating image with model: {self.model}, prompt: {prompt[:100]}...")

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                data = response.json()

                # Extract base64 image data
                image_b64 = data["data"][0]["b64_json"]
                image_bytes = base64.b64decode(image_b64)

                logger.info(f"Image generated successfully, size: {len(image_bytes)} bytes")
                return image_bytes

        except httpx.HTTPError as e:
            logger.error(f"HTTP error generating image: {e}")
            raise Exception(f"Failed to generate image: {e}")
        except Exception as e:
            logger.error(f"Error generating image: {e}")
            raise Exception(f"Failed to generate image: {e}")
