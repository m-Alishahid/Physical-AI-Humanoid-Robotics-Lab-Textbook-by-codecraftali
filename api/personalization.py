"""
Personalization endpoints
Adapts textbook content based on user profile using OpenAI
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging
import hashlib
import json

from .database import get_db, save_personalization, get_user_by_id
from .config import settings
from openai import OpenAI

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/personalization", tags=["personalization"])

openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)

# Pydantic models
class PersonalizationRequest(BaseModel):
    chapter: str
    original_content: str
    selected_text: Optional[str] = None

class PersonalizationResponse(BaseModel):
    personalized_content: str
    personalization_id: int
    applied_changes: Dict[str, Any]

# Personalization cache (in production, use Redis)
personalization_cache = {}

def get_cache_key(user_id: int, chapter: str, content_hash: str) -> str:
    """Generate cache key for personalization"""
    return f"{user_id}_{chapter}_{content_hash}"

def get_content_hash(content: str) -> str:
    """Generate hash for content"""
    return hashlib.md5(content.encode()).hexdigest()

def get_user_context(user_id: int, db: Session) -> Dict[str, Any]:
    """Get user context for personalization"""
    user = get_user_by_id(db, user_id)
    if not user:
        return {}

    return {
        "python_level": user.python_level,
        "robotics_experience": user.robotics_experience,
        "full_name": user.full_name,
        "user_id": user.id
    }

def create_personalization_prompt(
    original_content: str,
    user_context: Dict[str, Any],
    selected_text: Optional[str] = None
) -> str:
    """Create personalization prompt for OpenAI"""

    python_descriptions = {
        "beginner": "basic Python concepts, avoid advanced syntax",
        "intermediate": "standard Python features, some advanced concepts",
        "advanced": "advanced Python features, best practices",
        "expert": "expert-level Python, optimization, design patterns"
    }

    robotics_descriptions = {
        "none": "no robotics background, explain all concepts",
        "basic": "basic robotics knowledge, build on fundamentals",
        "intermediate": "good robotics understanding, technical depth",
        "advanced": "advanced robotics expertise, detailed technical content",
        "expert": "expert robotics knowledge, cutting-edge concepts"
    }

    prompt_parts = [
        "You are personalizing educational content for a robotics textbook.",
        "",
        f"User Profile:",
        f"- Python Level: {user_context.get('python_level', 'intermediate')} ({python_descriptions.get(user_context.get('python_level', 'intermediate'), 'standard level')})",
        f"- Robotics Experience: {user_context.get('robotics_experience', 'basic')} ({robotics_descriptions.get(user_context.get('robotics_experience', 'basic'), 'basic level')})",
        "",
        "Personalization Guidelines:",
        "1. Adjust technical depth based on user's Python and robotics experience",
        "2. Add explanations for concepts they might not know",
        "3. Skip or simplify explanations for concepts they already know",
        "4. Include practical examples appropriate to their skill level",
        "5. Maintain the educational value and accuracy of the content",
        "6. Keep the same overall structure and learning objectives",
        "7. Use appropriate terminology for their experience level",
        "",
        "Content to personalize:"
    ]

    if selected_text:
        prompt_parts.extend([
            f"Selected text: {selected_text}",
            "",
            "Full context:"
        ])

    prompt_parts.append(original_content)

    prompt_parts.extend([
        "",
        "Please provide the personalized version of this content:"
    ])

    return "\n".join(prompt_parts)

@router.post("/adapt", response_model=PersonalizationResponse)
async def adapt_content(
    request: PersonalizationRequest,
    user_id: int = None,
    db: Session = Depends(get_db)
):
    """Adapt content based on user profile"""
    try:
        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="Authentication required for personalization"
            )

        # Get user context
        user_context = get_user_context(user_id, db)
        if not user_context:
            raise HTTPException(
                status_code=404,
                detail="User profile not found"
            )

        # Check cache first
        content_hash = get_content_hash(request.original_content)
        cache_key = get_cache_key(user_id, request.chapter, content_hash)

        if cache_key in personalization_cache:
            cached_result = personalization_cache[cache_key]
            logger.info(f"Returning cached personalization for user {user_id}, chapter {request.chapter}")
            return PersonalizationResponse(
                personalized_content=cached_result["personalized_content"],
                personalization_id=cached_result["personalization_id"],
                applied_changes=cached_result["applied_changes"]
            )

        # Create personalization prompt
        prompt = create_personalization_prompt(
            request.original_content,
            user_context,
            request.selected_text
        )

        # Generate personalized content
        response = openai_client.chat.completions.create(
            model=settings.OPENAI_CHAT_MODEL,
            messages=[
                {"role": "system", "content": "You are an expert at personalizing educational content for different skill levels."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=settings.MAX_TOKENS,
            temperature=0.3  # Lower temperature for more consistent personalization
        )

        personalized_content = response.choices[0].message.content

        # Save personalization to database
        personalization_params = {
            "python_level": user_context.get("python_level"),
            "robotics_experience": user_context.get("robotics_experience"),
            "selected_text_provided": request.selected_text is not None
        }

        personalization_record = save_personalization(
            db=db,
            user_id=user_id,
            chapter=request.chapter,
            original_content=request.original_content,
            personalized_content=personalized_content,
            params=personalization_params
        )

        # Cache the result
        cache_result = {
            "personalized_content": personalized_content,
            "personalization_id": personalization_record.id,
            "applied_changes": personalization_params
        }
        personalization_cache[cache_key] = cache_result

        # Limit cache size (simple implementation)
        if len(personalization_cache) > 100:
            # Remove oldest entry (in production, use LRU cache)
            oldest_key = next(iter(personalization_cache))
            del personalization_cache[oldest_key]

        logger.info(f"Content personalized for user {user_id}, chapter {request.chapter}")

        return PersonalizationResponse(
            personalized_content=personalized_content,
            personalization_id=personalization_record.id,
            applied_changes=personalization_params
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Personalization error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error during personalization"
        )

@router.get("/history")
async def get_personalization_history(
    chapter: Optional[str] = None,
    limit: int = 20,
    user_id: int = None,
    db: Session = Depends(get_db)
):
    """Get personalization history for a user"""
    try:
        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="Authentication required"
            )

        from .database import PersonalizationHistory

        query = db.query(PersonalizationHistory).filter(
            PersonalizationHistory.user_id == user_id
        )

        if chapter:
            query = query.filter(PersonalizationHistory.chapter == chapter)

        history = query.order_by(PersonalizationHistory.created_at.desc()).limit(limit).all()

        return {
            "history": [
                {
                    "id": item.id,
                    "chapter": item.chapter,
                    "created_at": item.created_at,
                    "params": json.loads(item.personalization_params) if item.personalization_params else None
                }
                for item in history
            ]
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get personalization history error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error retrieving personalization history"
        )

@router.delete("/cache")
async def clear_personalization_cache(user_id: int = None):
    """Clear personalization cache (admin function)"""
    try:
        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="Authentication required"
            )

        # In production, only allow admins to clear cache
        # For now, clear user's cache entries
        keys_to_remove = [k for k in personalization_cache.keys() if k.startswith(f"{user_id}_")]
        for key in keys_to_remove:
            del personalization_cache[key]

        logger.info(f"Cleared personalization cache for user {user_id}")

        return {"message": f"Cleared {len(keys_to_remove)} cached personalizations"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Clear cache error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error clearing cache"
        )
