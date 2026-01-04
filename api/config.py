"""
Configuration settings for Physical AI Textbook API
Environment variables and application settings
"""

import os
from typing import List, Optional
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    """Application settings with environment variable support"""

    # FastAPI settings
    APP_NAME: str = "Physical AI Textbook API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = Field(default=False, env="DEBUG")

    # Server settings
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8000, env="PORT")

    # CORS settings
    ALLOWED_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://127.0.0.1:3000", "https://physical-ai-lab.vercel.app"],
        env="ALLOWED_ORIGINS"
    )

    # Database settings
    DATABASE_URL: str = Field(..., env="DATABASE_URL")  # Required
    DB_POOL_SIZE: int = Field(default=5, env="DB_POOL_SIZE")
    DB_MAX_OVERFLOW: int = Field(default=10, env="DB_MAX_OVERFLOW")

    # Vector database settings
    QDRANT_URL: str = Field(..., env="QDRANT_URL")  # Required
    QDRANT_API_KEY: str = Field(..., env="QDRANT_API_KEY")  # Required
    QDRANT_COLLECTION_NAME: str = Field(default="physical_ai_textbook", env="QDRANT_COLLECTION_NAME")

    # Gemini settings
    GEMINI_API_KEY: str = Field(..., env="GEMINI_API_KEY")  # Required
    GEMINI_CHAT_MODEL: str = Field(default="gemini-pro", env="GEMINI_CHAT_MODEL")
    GEMINI_EMBEDDING_MODEL: str = Field(default="text-embedding-004", env="GEMINI_EMBEDDING_MODEL")

    # Content processing settings
    CHUNK_SIZE: int = Field(default=1000, env="CHUNK_SIZE")
    CHUNK_OVERLAP: int = Field(default=200, env="CHUNK_OVERLAP")
    MAX_CONTEXT_CHUNKS: int = Field(default=3, env="MAX_CONTEXT_CHUNKS")
    SIMILARITY_THRESHOLD: float = Field(default=0.7, env="SIMILARITY_THRESHOLD")

    # Chatbot settings
    MAX_TOKENS: int = Field(default=1000, env="MAX_TOKENS")
    CHAT_TEMPERATURE: float = Field(default=0.7, env="CHAT_TEMPERATURE")

    # Authentication settings
    SECRET_KEY: str = Field(..., env="SECRET_KEY")  # Required
    ALGORITHM: str = Field(default="HS256", env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")

    # Rate limiting
    RATE_LIMIT_REQUESTS: int = Field(default=10, env="RATE_LIMIT_REQUESTS")
    RATE_LIMIT_WINDOW: int = Field(default=60, env="RATE_LIMIT_WINDOW")  # seconds

    # Translation settings
    DEFAULT_SOURCE_LANG: str = Field(default="en", env="DEFAULT_SOURCE_LANG")
    DEFAULT_TARGET_LANG: str = Field(default="ur", env="DEFAULT_TARGET_LANG")

    class Config:
        env_file = ".env"
        case_sensitive = False

# Create global settings instance
settings = Settings()
