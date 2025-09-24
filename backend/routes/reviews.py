"""
Review routes for product reviews and sentiment analysis
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from beanie import PydanticObjectId

from app.models.schemas import (
    ReviewCreate, Review as ReviewSchema, SentimentPredictionRequest,
    SentimentPredictionResponse
)
from app.models.mongodb_models import Review, Product, User
from app.services.auth_service import get_current_active_user, get_current_user_optional
from services.sentiment import analyze_sentiment

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.get("/product/{product_id}", response_model=List[ReviewSchema])
async def get_product_reviews(
    product_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    rating_filter: Optional[int] = Query(None, ge=1, le=5),
    sentiment_filter: Optional[str] = None
):
    """Get reviews for a specific product"""
    try:
        product_obj_id = PydanticObjectId(product_id)
        
        # Verify product exists
        product = await Product.get(product_obj_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        
        # Build query filter
        query_filter = {"product_id": product_obj_id}
        
        if rating_filter:
            query_filter["rating"] = rating_filter
        
        if sentiment_filter:
            query_filter["sentiment_label"] = sentiment_filter
        
        # Get reviews
        reviews = await Review.find(query_filter).skip(skip).limit(limit).to_list()
        
        return [
            ReviewSchema(
                id=str(review.id),
                product_id=str(review.product_id),
                platform=review.platform,
                reviewer_name=review.reviewer_name,
                rating=review.rating,
                title=review.title,
                content=review.content,
                helpful_votes=review.helpful_votes,
                verified_purchase=review.verified_purchase,
                review_date=review.review_date,
                sentiment_score=review.sentiment_score,
                sentiment_label=review.sentiment_label,
                created_at=review.created_at,
                updated_at=review.updated_at
            )
            for review in reviews
        ]
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid product ID"
        )


@router.get("/analysis/{product_id}")
async def review_analysis(product_id: str):
    """Get sentiment analysis and recommendations for a product"""
    sentiments = analyze_sentiment(product_id)
    return {"sentiments": sentiments, "product_id": product_id}
