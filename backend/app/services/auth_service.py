"""
Authentication and User Management Service
"""
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.config import settings
from app.models.mongodb_models import User, UserRole
from app.models.schemas import TokenData, UserCreate, UserLogin


# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Security
security = HTTPBearer()


class AuthService:
    """Authentication service for user management"""

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hash a password"""
        return pwd_context.hash(password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    @staticmethod
    def create_refresh_token(data: dict) -> str:
        """Create JWT refresh token"""
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_token(token: str) -> TokenData:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id: str = payload.get("sub")
            username: str = payload.get("username")
            
            if user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            token_data = TokenData(user_id=user_id, username=username)
            return token_data
            
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

    @staticmethod
    async def authenticate_user(username_or_email: str, password: str) -> Optional[User]:
        """Authenticate user with username/email and password"""
        # Try to find user by username or email
        user = await User.find_one(
            {"$or": [{"username": username_or_email}, {"email": username_or_email}]}
        )
        
        if not user:
            return None
        
        if not AuthService.verify_password(password, user.hashed_password):
            return None
        
        # Update last login
        user.last_login = datetime.now(timezone.utc)
        await user.save()
        
        return user

    @staticmethod
    async def create_user(user_data: UserCreate) -> User:
        """Create a new user"""
        # Check if username already exists
        existing_user = await User.find_one({"username": user_data.username})
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        # Check if email already exists
        existing_email = await User.find_one({"email": user_data.email})
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        hashed_password = AuthService.get_password_hash(user_data.password)
        
        user = User(
            username=user_data.username,
            email=user_data.email,
            full_name=user_data.full_name,
            hashed_password=hashed_password,
            phone_number=user_data.phone_number,
            date_of_birth=user_data.date_of_birth,
            role=UserRole.USER,
            is_active=True,
            is_verified=False
        )
        
        await user.insert()
        return user

    @staticmethod
    async def get_user_by_id(user_id: str) -> Optional[User]:
        """Get user by ID"""
        return await User.get(user_id)

    @staticmethod
    async def get_user_by_username(username: str) -> Optional[User]:
        """Get user by username"""
        return await User.find_one({"username": username})

    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        """Get user by email"""
        return await User.find_one({"email": email})

    @staticmethod
    async def update_user(user_id: str, update_data: dict) -> Optional[User]:
        """Update user data"""
        user = await User.get(user_id)
        if not user:
            return None
        
        # Update fields
        for field, value in update_data.items():
            if hasattr(user, field) and value is not None:
                setattr(user, field, value)
        
        user.updated_at = datetime.now(timezone.utc)
        await user.save()
        return user

    @staticmethod
    async def deactivate_user(user_id: str) -> bool:
        """Deactivate a user account"""
        user = await User.get(user_id)
        if not user:
            return False
        
        user.is_active = False
        user.updated_at = datetime.now(timezone.utc)
        await user.save()
        return True

    @staticmethod
    async def verify_user_email(user_id: str) -> bool:
        """Mark user email as verified"""
        user = await User.get(user_id)
        if not user:
            return False
        
        user.is_verified = True
        user.updated_at = datetime.now(timezone.utc)
        await user.save()
        return True


# Dependency to get current user
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Dependency to get current authenticated user"""
    token = credentials.credentials
    token_data = AuthService.verify_token(token)
    
    user = await AuthService.get_user_by_id(token_data.user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    return user


# Dependency to get current active user
async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Dependency to get current active user"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# Dependency for admin users only
async def get_current_admin_user(current_user: User = Depends(get_current_active_user)) -> User:
    """Dependency to get current admin user"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user


# Optional user dependency (for features that work with or without auth)
async def get_current_user_optional(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> Optional[User]:
    """Optional dependency to get current user"""
    if not credentials:
        return None
    
    try:
        token = credentials.credentials
        token_data = AuthService.verify_token(token)
        user = await AuthService.get_user_by_id(token_data.user_id)
        return user if user and user.is_active else None
    except HTTPException:
        return None