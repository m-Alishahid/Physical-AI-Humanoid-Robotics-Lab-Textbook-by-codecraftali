"""
RAG Chatbot endpoints
Provides conversational AI with textbook content context
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging
import json
from datetime import datetime

from .database import get_db, save_chat_message, get_user_by_id
from .vector_db import search_similar
from .config import settings
import google.generativeai as genai

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chatbot", tags=["chatbot"])

genai.configure(api_key=settings.GEMINI_API_KEY)

# Pydantic models
class ChatMessage(BaseModel):
    message: str
    session_id: str
    selected_text: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    context_chunks: List[Dict[str, Any]]
    session_id: str

class ChatHistory(BaseModel):
    session_id: str
    limit: int = 50

def get_user_context(user_id: int, db: Session) -> str:
    """Get user context for personalization"""
    user = get_user_by_id(db, user_id)
    if not user:
        return ""

    context = f"""
    User Profile:
    - Python Level: {user.python_level}
    - Robotics Experience: {user.robotics_experience}
    - Account Created: {user.created_at.strftime('%Y-%m-%d')}
    """

    if user.full_name:
        context += f"- Name: {user.full_name}"

    return context.strip()

def build_system_prompt(user_context: str = "") -> str:
    """Build system prompt for the chatbot"""
    base_prompt = """
    You are an AI assistant for the Physical AI & Humanoid Robotics Lab Textbook.
    You help students learn ROS 2, digital twins, NVIDIA Isaac, and humanoid robotics.

    Guidelines:
    - Provide accurate, helpful explanations
    - Use the provided context from the textbook
    - Be encouraging and supportive for learners
    - Include practical examples when relevant
    - Suggest next steps or related topics when appropriate
    - If you don't have enough context, suggest consulting the textbook chapters
    """

    if user_context:
        base_prompt += f"\n\nUser Context:\n{user_context}"

    return base_prompt.strip()

def build_context_prompt(query: str, context_chunks: List[Dict[str, Any]], selected_text: Optional[str] = None) -> str:
    """Build context prompt with relevant textbook content"""
    context_parts = []

    if selected_text:
        context_parts.append(f"Selected Text: {selected_text}")

    if context_chunks:
        context_parts.append("Relevant Textbook Content:")
        for i, chunk in enumerate(context_chunks, 1):
            context_parts.append(f"{i}. Chapter: {chunk.get('chapter', 'Unknown')}")
            context_parts.append(f"   Section: {chunk.get('section', 'Unknown')}")
            context_parts.append(f"   Content: {chunk.get('text', '')[:500]}...")
            context_parts.append("")

    context_parts.append(f"User Question: {query}")

    return "\n".join(context_parts)

@router.post("/chat", response_model=ChatResponse)
async def chat(
    chat_data: ChatMessage,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Main chat endpoint with RAG functionality"""
    try:
        # Get user context for personalization
        user_context = ""
        if user_id:
            user_context = get_user_context(user_id, db)

        # Search for relevant content
        search_query = chat_data.selected_text or chat_data.message
        context_chunks = search_similar(
            query=search_query,
            limit=settings.MAX_CONTEXT_CHUNKS,
            score_threshold=settings.SIMILARITY_THRESHOLD
        )

        # Build prompts
        system_prompt = build_system_prompt(user_context)
        context_prompt = build_context_prompt(
            chat_data.message,
            context_chunks,
            chat_data.selected_text
        )

        # Generate response using Gemini
        full_prompt = f"{system_prompt}\n\n{context_prompt}"

        model = genai.GenerativeModel(settings.GEMINI_CHAT_MODEL)
        response = model.generate_content(
            full_prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=settings.MAX_TOKENS,
                temperature=settings.CHAT_TEMPERATURE
            )
        )

        ai_response = response.text

        # Save chat history if user is authenticated
        if user_id:
            save_chat_message(
                db=db,
                user_id=user_id,
                session_id=chat_data.session_id,
                message=chat_data.message,
                response=ai_response,
                context_chunks=context_chunks
            )

        logger.info(f"Chat response generated for session {chat_data.session_id}")

        return ChatResponse(
            response=ai_response,
            context_chunks=context_chunks,
            session_id=chat_data.session_id
        )

    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error during chat processing"
        )

@router.get("/history/{session_id}")
async def get_chat_history(
    session_id: str,
    limit: int = 50,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get chat history for a session"""
    try:
        from .database import ChatHistory as ChatHistoryModel

        query = db.query(ChatHistoryModel).filter(
            ChatHistoryModel.session_id == session_id
        )

        if user_id:
            query = query.filter(ChatHistoryModel.user_id == user_id)

        history = query.order_by(ChatHistoryModel.created_at.desc()).limit(limit).all()

        return {
            "session_id": session_id,
            "messages": [
                {
                    "id": msg.id,
                    "message": msg.message,
                    "response": msg.response,
                    "created_at": msg.created_at,
                    "context_chunks": json.loads(msg.context_chunks) if msg.context_chunks else None
                }
                for msg in reversed(history)  # Return in chronological order
            ]
        }

    except Exception as e:
        logger.error(f"Chat history error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error retrieving chat history"
        )

@router.delete("/history/{session_id}")
async def clear_chat_history(
    session_id: str,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Clear chat history for a session"""
    try:
        from .database import ChatHistory as ChatHistoryModel

        query = db.query(ChatHistoryModel).filter(
            ChatHistoryModel.session_id == session_id
        )

        if user_id:
            query = query.filter(ChatHistoryModel.user_id == user_id)

        deleted_count = query.delete()
        db.commit()

        logger.info(f"Cleared {deleted_count} messages from session {session_id}")

        return {"message": f"Cleared {deleted_count} messages from chat history"}

    except Exception as e:
        logger.error(f"Clear chat history error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error clearing chat history"
        )

@router.get("/sessions")
async def get_chat_sessions(
    user_id: Optional[int] = None,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Get list of chat sessions for a user"""
    try:
        from .database import ChatHistory as ChatHistoryModel

        query = db.query(
            ChatHistoryModel.session_id,
            ChatHistoryModel.created_at
        ).distinct(ChatHistoryModel.session_id)

        if user_id:
            query = query.filter(ChatHistoryModel.user_id == user_id)

        sessions = query.order_by(ChatHistoryModel.created_at.desc()).limit(limit).all()

        return {
            "sessions": [
                {
                    "session_id": session.session_id,
                    "last_activity": session.created_at
                }
                for session in sessions
            ]
        }

    except Exception as e:
        logger.error(f"Get sessions error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error retrieving chat sessions"
        )
