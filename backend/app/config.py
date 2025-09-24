from pydantic_settings import BaseSettings
from pydantic import validator
from typing import List


class Settings(BaseSettings):
    # MongoDB Database (Atlas Configuration)
    MONGODB_URL: str = "mongodb+srv://<username>:<password>@<cluster>.mongodb.net/<database>?retryWrites=true&w=majority"
    DATABASE_NAME: str = "smartshopper"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production-super-secure-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    
    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:3000"
    
    def get_allowed_origins(self):
        if isinstance(self.ALLOWED_ORIGINS, str):
            return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(',')]
        return self.ALLOWED_ORIGINS
    
    # Scraping
    USER_AGENT: str = "SmartShopper/1.0"
    REQUEST_DELAY: float = 1.0
    
    # ML Model
    MODEL_PATH: str = "./models"
    
    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()