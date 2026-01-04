"""
Database connection and models for Neon Postgres
Handles user profiles and application data
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
import logging
from typing import Optional, Dict, Any
from datetime import datetime
import json

from .config import settings

logger = logging.getLogger(__name__)

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    echo=settings.DEBUG,
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

class UserProfile(Base):
    """User profile model with software/hardware background"""
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    # Profile information
    python_level = Column(Enum("beginner", "intermediate", "advanced", "expert", name="python_level"), nullable=False)
    robotics_experience = Column(Enum("none", "basic", "intermediate", "advanced", "expert", name="robotics_experience"), nullable=False)

    # Additional metadata
    full_name = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime)

    # Personalization preferences
    preferences = Column(Text)  # JSON string for flexible preferences

    def __repr__(self):
        return f"<UserProfile(email='{self.email}', python_level='{self.python_level}')>"

class ChatHistory(Base):
    """Chat history for RAG chatbot interactions"""
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    session_id = Column(String(255), index=True, nullable=False)
    message = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    context_chunks = Column(Text)  # JSON string of relevant chunks
    created_at = Column(DateTime, default=datetime.utcnow)

class PersonalizationHistory(Base):
    """History of personalization requests"""
    __tablename__ = "personalization_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    chapter = Column(String(255), nullable=False)
    original_content = Column(Text, nullable=False)
    personalized_content = Column(Text, nullable=False)
    personalization_params = Column(Text)  # JSON string of parameters used
    created_at = Column(DateTime, default=datetime.utcnow)

class TranslationCache(Base):
    """Cache for translation requests"""
    __tablename__ = "translation_cache"

    id = Column(Integer, primary_key=True, index=True)
    source_text_hash = Column(String(64), unique=True, index=True, nullable=False)
    source_text = Column(Text, nullable=False)
    translated_text = Column(Text, nullable=False)
    source_lang = Column(String(10), default="en")
    target_lang = Column(String(10), default="ur")
    created_at = Column(DateTime, default=datetime.utcnow)

# Dependency to get database session
def get_db() -> Session:
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def init_db():
    """Initialize database and create tables"""
    try:
        logger.info("Initializing database...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

# User profile operations
def create_user_profile(db: Session, email: str, hashed_password: str,
                       python_level: str, robotics_experience: str,
                       full_name: Optional[str] = None) -> UserProfile:
    """Create a new user profile"""
    user = UserProfile(
        email=email,
        hashed_password=hashed_password,
        python_level=python_level,
        robotics_experience=robotics_experience,
        full_name=full_name
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_email(db: Session, email: str) -> Optional[UserProfile]:
    """Get user profile by email"""
    return db.query(UserProfile).filter(UserProfile.email == email).first()

def get_user_by_id(db: Session, user_id: int) -> Optional[UserProfile]:
    """Get user profile by ID"""
    return db.query(UserProfile).filter(UserProfile.id == user_id).first()

def update_user_preferences(db: Session, user_id: int, preferences: Dict[str, Any]):
    """Update user preferences"""
    user = get_user_by_id(db, user_id)
    if user:
        user.preferences = json.dumps(preferences)
        user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(user)
    return user

# Chat history operations
def save_chat_message(db: Session, user_id: int, session_id: str,
                     message: str, response: str, context_chunks: Optional[list] = None):
    """Save a chat interaction"""
    chat = ChatHistory(
        user_id=user_id,
        session_id=session_id,
        message=message,
        response=response,
        context_chunks=json.dumps(context_chunks) if context_chunks else None
    )
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat

# Personalization operations
def save_personalization(db: Session, user_id: int, chapter: str,
                        original_content: str, personalized_content: str,
                        params: Dict[str, Any]):
    """Save personalization request"""
    personalization = PersonalizationHistory(
        user_id=user_id,
        chapter=chapter,
        original_content=original_content,
        personalized_content=personalized_content,
        personalization_params=json.dumps(params)
    )
    db.add(personalization)
    db.commit()
    db.refresh(personalization)
    return personalization

# Translation cache operations
def get_cached_translation(db: Session, text_hash: str) -> Optional[str]:
    """Get cached translation by text hash"""
    cache_entry = db.query(TranslationCache).filter(
        TranslationCache.source_text_hash == text_hash
    ).first()
    return cache_entry.translated_text if cache_entry else None

def save_translation_cache(db: Session, text_hash: str, source_text: str,
                          translated_text: str, source_lang: str = "en",
                          target_lang: str = "ur"):
    """Save translation to cache"""
    cache_entry = TranslationCache(
        source_text_hash=text_hash,
        source_text=source_text,
        translated_text=translated_text,
        source_lang=source_lang,
        target_lang=target_lang
    )
    db.add(cache_entry)
    db.commit()
    db.refresh(cache_entry)
    return cache_entry
