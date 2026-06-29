from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = Field(default="sqlite:///contentflow.db", description="Database connection URL")
    
    # Storage
    STORAGE_BASE_PATH: str = Field(default="../storage", description="Base path for storage directories")
    
    # Ollama (LLM)
    OLLAMA_BASE_URL: str = Field(default="http://localhost:11434", description="Ollama API base URL")
    OLLAMA_MODEL: str = Field(default="qwen2.5:7b", description="Ollama model to use")
    OLLAMA_TIMEOUT: int = Field(default=300, description="Ollama API timeout in seconds")
    
    # FLUX (Image Generation)
    FLUX_BASE_URL: str = Field(default="http://localhost:7860", description="FLUX API base URL")
    
    # Kokoro TTS (Voice Generation)
    KOKORO_BASE_URL: str = Field(default="http://localhost:8888", description="Kokoro TTS API base URL")
    
    # FFmpeg
    FFMPEG_PATH: str = Field(default="ffmpeg", description="Path to FFmpeg executable")
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
