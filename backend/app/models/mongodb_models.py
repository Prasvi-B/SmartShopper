"""
MongoDB Database Models using Beanie ODM
"""
from beanie import Document, Indexed
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from enum import Enum
import uuid


# Enums for better data integrity
class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"


class PlatformType(str, Enum):
    AMAZON = "amazon"
    FLIPKART = "flipkart"
    MYNTRA = "myntra"
    NYKAA = "nykaa"
    OTHER = "other"


class AlertStatus(str, Enum):
    ACTIVE = "active"
    TRIGGERED = "triggered"
    PAUSED = "paused"
    EXPIRED = "expired"


# User Model with Authentication
class User(Document):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    username: Indexed(str, unique=True)
    email: Indexed(EmailStr, unique=True)
    full_name: str
    hashed_password: str
    role: UserRole = UserRole.USER
    is_active: bool = True
    is_verified: bool = False
    avatar_url: Optional[str] = None
    phone_number: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_login: Optional[datetime] = None
    
    class Settings:
        name = "users"


# User Preferences
class UserPreferences(Document):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    user_id: Indexed(str)
    preferred_categories: List[str] = []
    preferred_brands: List[str] = []
    budget_range: Dict[str, float] = {"min": 0, "max": 100000}
    notification_settings: Dict[str, bool] = {
        "price_alerts": True,
        "deal_notifications": True,
        "email_updates": True,
        "sms_alerts": False
    }
    currency: str = "INR"
    language: str = "en"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    class Settings:
        name = "user_preferences"


# Enhanced Product Model
class Product(Document):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    name: Indexed(str)
    description: Optional[str] = None
    category: Indexed(str)
    brand: Indexed(str)
    image_url: Optional[str] = None
    sku: Optional[str] = None
    specifications: Dict[str, Any] = {}
    tags: List[str] = []
    avg_rating: float = 0.0
    total_reviews: int = 0
    min_price: float = 0.0
    max_price: float = 0.0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    class Settings:
        name = "products"


# Offer/Price Information
class Offer(Document):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    product_id: Indexed(str)
    platform: PlatformType
    url: str
    price: float
    original_price: Optional[float] = None
    discount_percentage: float = 0.0
    availability: str = "in_stock"
    seller_name: Optional[str] = None
    seller_rating: Optional[float] = None
    shipping_cost: float = 0.0
    delivery_time: Optional[str] = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    class Settings:
        name = "offers"


# Enhanced Review Model
class Review(Document):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    product_id: Indexed(str)
    user_id: Optional[Indexed(str)] = None
    platform: PlatformType
    reviewer_name: str
    rating: int = Field(ge=1, le=5)  # 1-5 stars
    review_text: str
    title: Optional[str] = None
    helpful_votes: int = 0
    total_votes: int = 0
    verified_purchase: bool = False
    review_date: datetime
    sentiment_score: Optional[float] = None  # -1 to 1
    sentiment_label: Optional[str] = None  # positive, negative, neutral
    images: List[str] = []
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    class Settings:
        name = "reviews"


# Price Alerts with User Integration
class PriceAlert(Document):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    user_id: Indexed(str)
    product_id: Indexed(str)
    target_price: float
    current_price: Optional[float] = None
    status: AlertStatus = AlertStatus.ACTIVE
    platform: Optional[PlatformType] = None
    notification_sent: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    triggered_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    
    class Settings:
        name = "price_alerts"


# User Wishlist
class Wishlist(Document):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    user_id: Indexed(str)
    name: str = "My Wishlist"
    description: Optional[str] = None
    is_public: bool = False
    products: List[Dict[str, Any]] = []  # List of {product_id, added_at, notes}
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    class Settings:
        name = "wishlists"


# Search History
class SearchHistory(Document):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    user_id: Optional[Indexed(str)] = None  # Can track anonymous searches too
    session_id: Optional[str] = None
    query: Indexed(str)
    filters: Dict[str, Any] = {}
    results_count: int = 0
    clicked_products: List[str] = []
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    class Settings:
        name = "search_history"