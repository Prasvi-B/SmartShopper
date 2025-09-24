from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from app.database.connection import init_db
from app.routes import products, reviews, search, alerts, auth, users
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown
    pass


app = FastAPI(
    title="SmartShopper API",
    description="Price comparison and review analysis API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1", tags=["authentication"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(search.router, prefix="/api/v1", tags=["search"])
app.include_router(products.router, prefix="/api/v1", tags=["products"])
app.include_router(reviews.router, prefix="/api/v1", tags=["reviews"])
app.include_router(alerts.router, prefix="/api/v1", tags=["alerts"])


@app.get("/")
async def root():
    return {"message": "SmartShopper API is running!"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )