"""
MongoDB Database Configuration and Connection
"""
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from typing import List
import asyncio

from app.config import settings


class Database:
    client: AsyncIOMotorClient = None
    database = None


db = Database()


async def connect_to_mongo():
    """Create database connection"""
    try:
        db.client = AsyncIOMotorClient(settings.MONGODB_URL)
        db.database = db.client[settings.DATABASE_NAME]
        
        # Import models here to avoid circular imports
        from app.models.database import (
            User, Product, Review, PriceAlert, 
            Wishlist, SearchHistory, UserPreferences
        )
        
        # Initialize Beanie with document models
        await init_beanie(
            database=db.database,
            document_models=[
                User,
                Product, 
                Review,
                PriceAlert,
                Wishlist,
                SearchHistory,
                UserPreferences
            ]
        )
        
        print(f"✅ Connected to MongoDB: {settings.DATABASE_NAME}")
        
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        raise e


async def init_db():
    """Initialize database connection and setup"""
    await connect_to_mongo()
    await create_indexes()


async def close_mongo_connection():
    """Close database connection"""
    if db.client:
        db.client.close()
        print("❌ Disconnected from MongoDB")


async def ping_database():
    """Check database connection"""
    try:
        await db.client.admin.command('ping')
        return True
    except Exception:
        return False


async def create_indexes():
    """Create database indexes for better performance"""
    try:
        # Import models here to avoid circular imports
        from app.models.database import (
            User, Product, Review, PriceAlert, 
            Wishlist, SearchHistory, UserPreferences
        )
        
        # User indexes
        await User.find().create_index("email", unique=True)
        await User.find().create_index("username", unique=True)
        
        # Product indexes
        await Product.find().create_index("name")
        await Product.find().create_index("category")
        await Product.find().create_index("brand")
        await Product.find().create_index([("name", "text"), ("description", "text")])
        
        # Review indexes
        await Review.find().create_index("product_id")
        await Review.find().create_index("user_id")
        await Review.find().create_index("rating")
        
        # Price Alert indexes
        await PriceAlert.find().create_index("user_id")
        await PriceAlert.find().create_index("product_id")
        await PriceAlert.find().create_index("is_active")
        
        # Wishlist indexes
        await Wishlist.find().create_index("user_id")
        
        # Search History indexes
        await SearchHistory.find().create_index("user_id")
        await SearchHistory.find().create_index("created_at")
        
        print("✅ Database indexes created successfully")
        
    except Exception as e:
        print(f"⚠️ Index creation warning: {e}")


# Database dependency for FastAPI
async def get_database():
    return db.database