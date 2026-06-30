import os
import logging
from sqlalchemy.orm import Session
from typing import List, Optional
from app.modules.voice.models import Voice
from app.modules.voice.schemas import VoiceCreate
from app.modules.scene.models import Scene
from app.shared.ai.orpheus_tts_client import OrpheusTTSClient
from app.config import settings

logger = logging.getLogger(__name__)


class VoiceService:
    """Service for voice/audio operations"""

    def __init__(self, db: Session, tts_client: Optional[OrpheusTTSClient] = None, language: str = "Hindi"):
        self.db = db
        self.language = language
        self.tts_client = tts_client or OrpheusTTSClient(language=language)

    def get_voices(self, project_id: str) -> List[Voice]:
        """Get all voices for a project"""
        return self.db.query(Voice).filter(Voice.project_id == project_id).all()

    def create_voice(self, voice_data: VoiceCreate) -> Voice:
        """Create a single voice record"""
        voice = Voice(
            scene_id=voice_data.scene_id,
            project_id=voice_data.project_id,
            file_path=voice_data.file_path,
            voice_used=voice_data.voice_used,
            text_used=voice_data.text_used,
            duration=voice_data.duration
        )
        self.db.add(voice)
        self.db.commit()
        self.db.refresh(voice)
        return voice

    def delete_voices(self, project_id: str) -> bool:
        """Delete all voices for a project"""
        voices = self.get_voices(project_id)
        for voice in voices:
            # Delete file from disk
            if os.path.exists(voice.file_path):
                try:
                    os.remove(voice.file_path)
                except Exception as e:
                    logger.error(f"Failed to delete voice file {voice.file_path}: {e}")
            self.db.delete(voice)
        self.db.commit()
        return True

    async def generate_voices(self, project_id: str, user_instructions: Optional[str] = None) -> List[Voice]:
        """Generate voices for all scenes in a project"""
        logger.info(f"Generating voices for project: {project_id}")

        # Get all scenes for the project
        scenes = self.db.query(Scene).filter(Scene.project_id == project_id).order_by(Scene.scene_number).all()

        if not scenes:
            raise ValueError("No scenes found for project")

        # Delete existing voices
        self.delete_voices(project_id)

        # Create project storage directory
        project_storage = os.path.join(settings.STORAGE_BASE_PATH, "projects", project_id, "voice")
        os.makedirs(project_storage, exist_ok=True)

        created_voices = []

        for idx, scene in enumerate(scenes):
            try:
                logger.info(f"Generating voice for scene {idx + 1}: {scene.title}")

                # Generate audio using Orpheus TTS
                # Use Hindi voice for Hindi content
                voice_name = "ऋतिका"  # Hindi female voice
                audio_bytes = await self.tts_client.generate(text=scene.voiceover_text, voice=voice_name)

                # Save audio to disk
                file_name = f"scene_{scene.scene_number:02d}.wav"
                file_path = os.path.join(project_storage, file_name)
                with open(file_path, "wb") as f:
                    f.write(audio_bytes)

                # Create voice record
                voice_create = VoiceCreate(
                    scene_id=scene.id,
                    project_id=project_id,
                    file_path=file_path,
                    voice_used=voice_name,
                    text_used=scene.voiceover_text
                )
                voice = self.create_voice(voice_create)
                created_voices.append(voice)

                logger.info(f"Voice generated for scene {idx + 1}: {file_path}")

            except Exception as e:
                logger.error(f"Failed to generate voice for scene {idx + 1}: {e}")
                raise Exception(f"Failed to generate voice for scene {idx + 1}: {e}")

        logger.info(f"Generated {len(created_voices)} voices for project {project_id}")

        # Refresh all voices from database to ensure they're attached to session
        for voice in created_voices:
            self.db.refresh(voice)

        return created_voices

    async def generate_voice_for_scene(self, project_id: str, scene_id: str) -> Voice:
        """Generate a single voice for a specific scene"""
        logger.info(f"Generating voice for scene {scene_id} in project {project_id}")

        # Get the scene
        scene = self.db.query(Scene).filter(Scene.id == scene_id, Scene.project_id == project_id).first()
        if not scene:
            raise ValueError(f"Scene {scene_id} not found in project {project_id}")

        # Check if voice already exists for this scene
        existing_voice = self.db.query(Voice).filter(Voice.scene_id == scene_id).first()
        if existing_voice:
            # Delete existing voice and file
            if os.path.exists(existing_voice.file_path):
                try:
                    os.remove(existing_voice.file_path)
                except Exception as e:
                    logger.error(f"Failed to delete existing voice file: {e}")
            self.db.delete(existing_voice)
            self.db.commit()

        # Create project storage directory
        project_storage = os.path.join(settings.STORAGE_BASE_PATH, "projects", project_id, "voice")
        os.makedirs(project_storage, exist_ok=True)

        # Generate audio using gTTS
        audio_bytes = await self.tts_client.generate(text=scene.voiceover_text)

        # Save audio to disk (MP3 format from gTTS)
        file_name = f"scene_{scene.scene_number:02d}.mp3"
        file_path = os.path.join(project_storage, file_name)
        with open(file_path, "wb") as f:
            f.write(audio_bytes)

        # Create voice record
        voice_create = VoiceCreate(
            scene_id=scene.id,
            project_id=project_id,
            file_path=file_path,
            voice_used=f"gTTS-{self.language}",
            text_used=scene.voiceover_text
        )
        voice = self.create_voice(voice_create)

        logger.info(f"Voice generated for scene {scene.scene_number}: {file_path}")

        # Refresh to ensure attached to session
        self.db.refresh(voice)

        return voice

    async def regenerate_voice(self, voice_id: str, new_text: str) -> Optional[Voice]:
        """Regenerate a single voice with new text"""
        voice = self.db.query(Voice).filter(Voice.id == voice_id).first()
        if not voice:
            return None

        try:
            logger.info(f"Regenerating voice {voice_id} with new text")

            # Get the scene
            scene = self.db.query(Scene).filter(Scene.id == voice.scene_id).first()
            if not scene:
                raise ValueError(f"Scene {voice.scene_id} not found")

            # Delete existing voice file
            if os.path.exists(voice.file_path):
                try:
                    os.remove(voice.file_path)
                except Exception as e:
                    logger.error(f"Failed to delete existing voice file: {e}")

            # Generate new audio
            voice_name = "ऋतिका"  # Hindi female voice
            audio_bytes = await self.tts_client.generate(text=new_text, voice=voice_name)

            # Save new audio
            file_path = voice.file_path
            with open(file_path, "wb") as f:
                f.write(audio_bytes)

            # Update voice record
            voice.text_used = new_text
            voice.file_path = file_path
            self.db.commit()
            self.db.refresh(voice)

            logger.info(f"Voice regenerated successfully: {file_path}")
            return voice

        except Exception as e:
            logger.error(f"Failed to regenerate voice: {e}")
            raise Exception(f"Failed to regenerate voice: {str(e)}")

    def approve_voices(self, project_id: str) -> List[Voice]:
        """Approve all voices for a project"""
        voices = self.get_voices(project_id)
        for voice in voices:
            voice.is_approved = True
        self.db.commit()
        for voice in voices:
            self.db.refresh(voice)
        return voices
