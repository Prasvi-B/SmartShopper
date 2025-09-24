from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from beanie import PydanticObjectId

from app.models.database import Review, Product, User
from app.models.schemas import (
    ReviewResponse, ReviewCreate, ReviewUpdate
)
from app.services.auth_service import get_current_user

router = APIRouter()


@router.get("/products/{product_id}/reviews", response_model=List[ReviewResponse])
async def get_product_reviews(
    product_id: PydanticObjectId,
    skip: int = 0,
    limit: int = 10,
    platform: Optional[str] = None
):
    """Get reviews for a specific product"""
    # Verify product exists
    product = await Product.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    query = {"product_id": product_id}
    if platform:
        query["platform"] = platform
    
    reviews = await Review.find(query).skip(skip).limit(limit).to_list()
    return reviews


@router.post("/products/{product_id}/reviews", response_model=ReviewResponse)
async def create_review(
    product_id: PydanticObjectId,
    review_data: ReviewCreate,
    current_user: User = Depends(get_current_user)
):
    """Create a new review for a product"""
    # Verify product exists
    product = await Product.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if user already reviewed this product
    existing_review = await Review.find_one({
        "product_id": product_id,
        "user_id": current_user.id
    })
    if existing_review:
        raise HTTPException(
            status_code=400, 
            detail="You have already reviewed this product"
        )
    
    # Create new review
    review = Review(
        **review_data.model_dump(),
        product_id=product_id,
        user_id=current_user.id
    )
    await review.insert()
    return review