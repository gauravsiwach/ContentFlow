from gtts import gTTS
import logging
import io

logger = logging.getLogger(__name__)


class OrpheusTTSClient:
    """Client for Text-to-Speech using gTTS (Google TTS)"""

    # Language code mappings
    LANGUAGE_CODES = {
        "Hindi": "hi",
        "hindi": "hi",
        "English": "en",
        "english": "en",
    }

    def __init__(self, language: str = "Hindi"):
        self.language = language
        self.lang_code = self.LANGUAGE_CODES.get(language, "hi")

    async def generate(self, text: str, voice: str = None) -> bytes:
        """
        Generate audio from text using gTTS

        Args:
            text: The text to convert to speech
            voice: The voice to use (not used by gTTS, kept for compatibility)

        Returns:
            Audio data as bytes (MP3 format)
        """
        try:
            logger.info(f"Generating TTS with gTTS, language: {self.language} ({self.lang_code}), text length: {len(text)}")

            # Create gTTS object
            tts = gTTS(text=text, lang=self.lang_code, slow=False)

            # Save to bytes buffer
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            audio_bytes = audio_buffer.read()

            logger.info(f"TTS generated successfully, size: {len(audio_bytes)} bytes")
            return audio_bytes

        except Exception as e:
            logger.error(f"Error during TTS generation: {e}")
            raise Exception(f"TTS generation failed: {str(e)}")
