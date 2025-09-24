"""
SmartShopper FastAPI Application with MongoDB
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from app.database.connection import init_db, close_mongo_connection
from app.routes import auth, user_features, products, reviews, search, alerts
from app.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting SmartShopper API...")
    try:
        await init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.warning(f"Failed to initialize database: {e}")
        logger.warning("Continuing without database connection...")
    
    yield
    
    # Shutdown
    logger.info("Shutting down SmartShopper API...")
    await close_mongo_connection()


# Create FastAPI application
app = FastAPI(
    title="SmartShopper API",
    description="Intelligent e-commerce price comparison and sentiment analysis platform",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "SmartShopper API",
        "version": "2.0.0"
    }


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to SmartShopper API",
        "version": "2.0.0",
        "description": "Intelligent e-commerce price comparison and sentiment analysis platform",
        "docs": "/docs",
        "health": "/health"
    }


# Include routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(user_features.router, prefix="/api/v1")
app.include_router(search.router, prefix="/api/v1")
app.include_router(products.router, prefix="/api/v1")
app.include_router(reviews.router, prefix="/api/v1")
app.include_router(alerts.router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
