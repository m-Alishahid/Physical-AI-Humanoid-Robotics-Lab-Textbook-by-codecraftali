"""
Authentication endpoints using better-auth
Handles user registration, login, and profile management
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from typing import Optional
import jwt
import logging

from .database import get_db, create_user_profile, get_user_by_email, get_user_by_id
from .config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["authentication"])

# Password hashing
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Pydantic models
class UserSignup(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    python_level: str  # beginner, intermediate, advanced, expert
    robotics_experience: str  # none, basic, intermediate, advanced, expert

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict

class UserProfileResponse(BaseModel):
    id: int
    email: str
    full_name: Optional[str]
    python_level: str
    robotics_experience: str
    created_at: datetime
    last_login: Optional[datetime]

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    python_level: Optional[str] = None
    robotics_experience: Optional[str] = None

# Helper functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def authenticate_user(db: Session, email: str, password: str):
    """Authenticate a user"""
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# API endpoints
@router.post("/signup", response_model=TokenResponse)
async def signup(user_data: UserSignup, db: Session = Depends(get_db)):
    """Create a new user account"""
    try:
        # Check if user already exists
        existing_user = get_user_by_email(db, user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Validate enum values
        valid_python_levels = ["beginner", "intermediate", "advanced", "expert"]
        valid_robotics_levels = ["none", "basic", "intermediate", "advanced", "expert"]

        if user_data.python_level not in valid_python_levels:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid python_level. Must be one of: {valid_python_levels}"
            )

        if user_data.robotics_experience not in valid_robotics_levels:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid robotics_experience. Must be one of: {valid_robotics_levels}"
            )

        # Create user
        hashed_password = get_password_hash(user_data.password)
        user = create_user_profile(
            db=db,
            email=user_data.email,
            hashed_password=hashed_password,
            python_level=user_data.python_level,
            robotics_experience=user_data.robotics_experience,
            full_name=user_data.full_name
        )

        # Create access token
        access_token = create_access_token(data={"sub": str(user.id)})

        logger.info(f"New user registered: {user.email}")

        return TokenResponse(
            access_token=access_token,
            user={
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "python_level": user.python_level,
                "robotics_experience": user.robotics_experience,
                "created_at": user.created_at.isoformat()
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Signup error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during signup"
        )

@router.post("/login", response_model=TokenResponse)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Authenticate user and return access token"""
    try:
        user = authenticate_user(db, user_credentials.email, user_credentials.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Update last login
        user.last_login = datetime.utcnow()
        db.commit()

        # Create access token
        access_token = create_access_token(data={"sub": str(user.id)})

        logger.info(f"User logged in: {user.email}")

        return TokenResponse(
            access_token=access_token,
            user={
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "python_level": user.python_level,
                "robotics_experience": user.robotics_experience,
                "created_at": user.created_at.isoformat(),
                "last_login": user.last_login.isoformat() if user.last_login else None
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during login"
        )

@router.get("/profile", response_model=UserProfileResponse)
async def get_profile(user_id: int = None, db: Session = Depends(get_db)):
    """Get user profile information"""
    try:
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required"
            )

        user = get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return UserProfileResponse(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            python_level=user.python_level,
            robotics_experience=user.robotics_experience,
            created_at=user.created_at,
            last_login=user.last_login
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get profile error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error retrieving profile"
        )

@router.put("/profile", response_model=UserProfileResponse)
async def update_profile(
    user_update: UserUpdate,
    user_id: int = None,
    db: Session = Depends(get_db)
):
    """Update user profile information"""
    try:
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required"
            )

        user = get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Validate enum values if provided
        if user_update.python_level:
            valid_python_levels = ["beginner", "intermediate", "advanced", "expert"]
            if user_update.python_level not in valid_python_levels:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid python_level. Must be one of: {valid_python_levels}"
                )
            user.python_level = user_update.python_level

        if user_update.robotics_experience:
            valid_robotics_levels = ["none", "basic", "intermediate", "advanced", "expert"]
            if user_update.robotics_experience not in valid_robotics_levels:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid robotics_experience. Must be one of: {valid_robotics_levels}"
                )
            user.robotics_experience = user_update.robotics_experience

        if user_update.full_name is not None:
            user.full_name = user_update.full_name

        user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(user)

        logger.info(f"User profile updated: {user.email}")

        return UserProfileResponse(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            python_level=user.python_level,
            robotics_experience=user.robotics_experience,
            created_at=user.created_at,
            last_login=user.last_login
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Update profile error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error updating profile"
        )

@router.post("/logout")
async def logout():
    """Logout endpoint (client-side token removal)"""
    # In a stateless JWT system, logout is handled client-side
    # This endpoint can be used for any server-side cleanup if needed
    return {"message": "Logged out successfully"}
