"""
Authentication routes for user management
"""
from datetime import timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from app.models.schemas import (
    UserCreate, UserLogin, UserResponse, UserUpdate, UserWithPreferences, 
    UserPreferencesUpdate, Token, RefreshTokenRequest
)
from app.services.auth_service import (
    AuthService, get_current_user, get_current_active_user, 
    get_current_admin_user, security
)
from app.models.mongodb_models import User, UserPreferences
from app.config import settings

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate):
    """Register a new user"""
    user = await AuthService.create_user(user_data)
    return UserResponse(
        id=str(user.id),
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        phone_number=user.phone_number,
        date_of_birth=user.date_of_birth,
        role=user.role,
        is_active=user.is_active,
        is_verified=user.is_verified,
        created_at=user.created_at,
        last_login=user.last_login
    )


@router.post("/login", response_model=Token)
async def login_user(user_credentials: UserLogin):
    """Login user and return JWT tokens"""
    user = await AuthService.authenticate_user(
        user_credentials.username_or_email, 
        user_credentials.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username/email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access and refresh tokens
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = AuthService.create_access_token(
        data={"sub": str(user.id), "username": user.username},
        expires_delta=access_token_expires
    )
    
    refresh_token = AuthService.create_refresh_token(
        data={"sub": str(user.id), "username": user.username}
    )
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_request: RefreshTokenRequest):
    """Refresh access token using refresh token"""
    try:
        token_data = AuthService.verify_token(refresh_request.refresh_token)
        user = await AuthService.get_user_by_id(token_data.user_id)
        
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        # Create new access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = AuthService.create_access_token(
            data={"sub": str(user.id), "username": user.username},
            expires_delta=access_token_expires
        )
        
        # Create new refresh token
        refresh_token = AuthService.create_refresh_token(
            data={"sub": str(user.id), "username": user.username}
        )
        
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
        
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )


@router.get("/me", response_model=UserWithPreferences)
async def get_current_user_profile(current_user: User = Depends(get_current_active_user)):
    """Get current user profile with preferences"""
    # Get user preferences
    preferences = await UserPreferences.find_one({"user_id": current_user.id})
    
    return UserWithPreferences(
        id=str(current_user.id),
        username=current_user.username,
        email=current_user.email,
        full_name=current_user.full_name,
        phone_number=current_user.phone_number,
        date_of_birth=current_user.date_of_birth,
        role=current_user.role,
        is_active=current_user.is_active,
        is_verified=current_user.is_verified,
        created_at=current_user.created_at,
        last_login=current_user.last_login,
        preferences=preferences.dict() if preferences else None
    )


@router.patch("/me", response_model=UserResponse)
async def update_current_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """Update current user profile"""
    update_data = user_update.dict(exclude_unset=True)
    
    updated_user = await AuthService.update_user(str(current_user.id), update_data)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse(
        id=str(updated_user.id),
        username=updated_user.username,
        email=updated_user.email,
        full_name=updated_user.full_name,
        phone_number=updated_user.phone_number,
        date_of_birth=updated_user.date_of_birth,
        role=updated_user.role,
        is_active=updated_user.is_active,
        is_verified=updated_user.is_verified,
        created_at=updated_user.created_at,
        last_login=updated_user.last_login
    )


@router.patch("/me/preferences")
async def update_user_preferences(
    preferences_update: UserPreferencesUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """Update user preferences"""
    # Find existing preferences or create new ones
    preferences = await UserPreferences.find_one({"user_id": current_user.id})
    
    if not preferences:
        # Create new preferences
        preferences = UserPreferences(
            user_id=current_user.id,
            **preferences_update.dict(exclude_unset=True)
        )
        await preferences.insert()
    else:
        # Update existing preferences
        update_data = preferences_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(preferences, field):
                setattr(preferences, field, value)
        await preferences.save()
    
    return {"message": "Preferences updated successfully"}


@router.post("/logout")
async def logout_user(current_user: User = Depends(get_current_active_user)):
    """Logout user (client should delete tokens)"""
    return {"message": "Successfully logged out"}


@router.post("/verify-email/{user_id}")
async def verify_user_email(
    user_id: str,
    admin_user: User = Depends(get_current_admin_user)
):
    """Verify user email (admin only)"""
    success = await AuthService.verify_user_email(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {"message": "User email verified successfully"}


@router.post("/deactivate/{user_id}")
async def deactivate_user(
    user_id: str,
    admin_user: User = Depends(get_current_admin_user)
):
    """Deactivate user account (admin only)"""
    success = await AuthService.deactivate_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {"message": "User deactivated successfully"}


@router.get("/users", response_model=list[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    admin_user: User = Depends(get_current_admin_user)
):
    """List all users (admin only)"""
    users = await User.find_all().skip(skip).limit(limit).to_list()
    
    return [
        UserResponse(
            id=str(user.id),
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            phone_number=user.phone_number,
            date_of_birth=user.date_of_birth,
            role=user.role,
            is_active=user.is_active,
            is_verified=user.is_verified,
            created_at=user.created_at,
            last_login=user.last_login
        )
        for user in users
    ]


@router.get("/users/{user_id}", response_model=UserWithPreferences)
async def get_user_by_id(
    user_id: str,
    admin_user: User = Depends(get_current_admin_user)
):
    """Get user by ID (admin only)"""
    user = await AuthService.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get user preferences
    preferences = await UserPreferences.find_one({"user_id": user.id})
    
    return UserWithPreferences(
        id=str(user.id),
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        phone_number=user.phone_number,
        date_of_birth=user.date_of_birth,
        role=user.role,
        is_active=user.is_active,
        is_verified=user.is_verified,
        created_at=user.created_at,
        last_login=user.last_login,
        preferences=preferences.dict() if preferences else None
    )