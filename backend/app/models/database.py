"""
MongoDB Database Models using Beanie ODM
"""
from datetime import datetime
from typing import List, Optional
from beanie import Document, Indexed
from pydantic import Field, EmailStr
from bson import ObjectId


# User Model
class User(Document):
    username: str = Field(..., unique=True)
    email: EmailStr = Field(..., unique=True)
    hashed_password: str
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    is_active: bool = True
    is_verified: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "users"


# User Preferences Model
class UserPreferences(Document):
    user_id: str
    preferred_categories: List[str] = []
    preferred_brands: List[str] = []
    price_range_min: Optional[float] = None
    price_range_max: Optional[float] = None
    notification_settings: dict = {}
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "user_preferences"


# Product Model
class Product(Document):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    image_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "products"


# Offer Model
class Offer(Document):
    product_id: str
    platform: str  # amazon, flipkart, etc.
    url: str
    price: float
    original_price: Optional[float] = None
    discount_percentage: Optional[float] = None
    availability: bool = True
    shipping_cost: Optional[float] = None
    delivery_time: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "offers"


# Review Model  
class Review(Document):
    product_id: str
    user_id: Optional[str] = None
    platform: str
    rating: float = Field(ge=1, le=5)
    title: Optional[str] = None
    content: str
    helpful_votes: int = 0
    total_votes: int = 0
    verified_purchase: bool = False
    sentiment_score: Optional[float] = None
    sentiment_label: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "reviews"


# Price Alert Model
class PriceAlert(Document):
    user_id: str
    product_id: str
    target_price: float
    current_price: Optional[float] = None
    is_active: bool = True
    notification_sent: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    triggered_at: Optional[datetime] = None
    
    class Settings:
        name = "price_alerts"


# Wishlist Model
class Wishlist(Document):
    user_id: str
    name: str = "My Wishlist"
    products: List[str] = []  # List of product IDs
    is_public: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "wishlists"


# Search History Model
class SearchHistory(Document):
    user_id: str
    query: str
    filters: dict = {}
    results_count: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "search_history"