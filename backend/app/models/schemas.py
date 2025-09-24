from pydantic import BaseModel, Field, EmailStr, validator
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from enum import Enum


class SentimentLabel(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


class Platform(str, Enum):
    AMAZON = "amazon"
    FLIPKART = "flipkart"
    MYNTRA = "myntra"


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"


# Authentication Models
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = Field(None, max_length=100)
    phone_number: Optional[str] = Field(None, pattern=r'^\+?1?\d{9,15}$')
    date_of_birth: Optional[date] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class UserLogin(BaseModel):
    username_or_email: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, max_length=100)
    phone_number: Optional[str] = Field(None, pattern=r'^\+?1?\d{9,15}$')
    date_of_birth: Optional[date] = None


class UserPreferencesUpdate(BaseModel):
    preferred_categories: Optional[List[str]] = None
    preferred_brands: Optional[List[str]] = None
    price_range_min: Optional[float] = Field(None, ge=0)
    price_range_max: Optional[float] = Field(None, ge=0)
    preferred_platforms: Optional[List[Platform]] = None
    email_notifications: Optional[bool] = True
    push_notifications: Optional[bool] = True
    newsletter_subscription: Optional[bool] = True


class UserResponse(UserBase):
    id: str
    role: UserRole
    is_active: bool
    is_verified: bool
    created_at: datetime
    last_login: Optional[datetime] = None


class UserWithPreferences(UserResponse):
    preferences: Optional[Dict[str, Any]] = None


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModel):
    user_id: Optional[str] = None
    username: Optional[str] = None


class RefreshTokenRequest(BaseModel):
    refresh_token: str


# Product Models
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    image_url: Optional[str] = None


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ProductResponse(Product):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    image_url: Optional[str] = None


# Offer Models
class OfferBase(BaseModel):
    platform: Platform
    url: str
    price: float
    original_price: Optional[float] = None
    discount_percentage: Optional[float] = None
    availability: str = "in_stock"
    seller_name: Optional[str] = None
    shipping_cost: float = 0.0


class OfferCreate(OfferBase):
    product_id: str


class Offer(OfferBase):
    id: str
    product_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Review Models
class ReviewBase(BaseModel):
    platform: Platform
    reviewer_name: Optional[str] = None
    rating: int = Field(..., ge=1, le=5)
    title: Optional[str] = None
    content: str
    helpful_votes: int = 0
    verified_purchase: bool = False
    review_date: Optional[datetime] = None


class ReviewCreate(ReviewBase):
    product_id: str


class Review(ReviewBase):
    id: str
    product_id: str
    sentiment_score: Optional[float] = None
    sentiment_label: Optional[SentimentLabel] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ReviewResponse(Review):
    pass


class ReviewUpdate(BaseModel):
    rating: Optional[float] = Field(None, ge=1, le=5)
    title: Optional[str] = None
    content: Optional[str] = None


# Search Models
class SearchQuery(BaseModel):
    query: str
    category: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    platform: Optional[Platform] = None


class ProductSummary(BaseModel):
    id: str
    name: str
    description: Optional[str]
    brand: Optional[str]
    image_url: Optional[str]
    min_price: float
    max_price: float
    avg_rating: float
    total_reviews: int
    best_offer: Offer
    sentiment_summary: dict


class SearchResponse(BaseModel):
    products: List[ProductSummary]
    total_count: int
    query: str


# Alert Models
class PriceAlertCreate(BaseModel):
    product_id: str
    target_price: float


class PriceAlert(BaseModel):
    id: str
    product_id: str
    user_id: str
    target_price: float
    is_active: bool
    created_at: datetime
    last_checked: Optional[datetime]
    
    class Config:
        from_attributes = True


class PriceAlertResponse(PriceAlert):
    pass


class PriceAlertUpdate(BaseModel):
    target_price: Optional[float] = None
    is_active: Optional[bool] = None


# User Feature Models
class WishlistItemCreate(BaseModel):
    product_id: str


class WishlistItem(BaseModel):
    id: str
    product_id: str
    user_id: str
    created_at: datetime


class SearchHistoryItem(BaseModel):
    id: str
    user_id: str
    query: str
    results_count: int
    created_at: datetime


class SearchHistoryResponse(SearchHistoryItem):
    pass


# ML Models
class SentimentPredictionRequest(BaseModel):
    reviews: List[str]


class SentimentPrediction(BaseModel):
    text: str
    sentiment: SentimentLabel
    confidence: float


class SentimentPredictionResponse(BaseModel):
    predictions: List[SentimentPrediction]