from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from beanie import PydanticObjectId

from app.models.database import Product, SearchHistory, User
from app.models.schemas import ProductResponse, SearchHistoryResponse
from app.services.auth_service import get_current_user

router = APIRouter()


@router.get("/search", response_model=List[ProductResponse])
async def search_products(
    q: str = Query(..., description="Search query"),
    category: Optional[str] = None,
    brand: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    platform: Optional[str] = None,
    skip: int = 0,
    limit: int = 20,
    current_user: Optional[User] = Depends(get_current_user)
):
    """Search for products across platforms"""
    # Build search query
    query = {"$text": {"$search": q}}
    filters = {}
    
    if category:
        filters["category"] = category
    if brand:
        filters["brand"] = brand
    if platform:
        filters["platform"] = platform
    
    # Price range filter
    if min_price is not None or max_price is not None:
        price_filter = {}
        if min_price is not None:
            price_filter["$gte"] = min_price
        if max_price is not None:
            price_filter["$lte"] = max_price
        filters["price"] = price_filter
    
    # Combine search query with filters
    if filters:
        final_query = {"$and": [query, filters]}
    else:
        final_query = query
    
    # Search products
    products = await Product.find(final_query).skip(skip).limit(limit).to_list()
    
    # Save search history if user is authenticated
    if current_user:
        await SearchHistory(
            user_id=current_user.id,
            query=q,
            filters=filters,
            results_count=len(products)
        ).insert()
    
    return products


@router.get("/search/suggestions")
async def get_search_suggestions(
    q: str = Query(..., description="Partial search query"),
    limit: int = 10
):
    """Get search suggestions based on partial query"""
    # Search in product names and categories
    suggestions = await Product.find({
        "$or": [
            {"name": {"$regex": q, "$options": "i"}},
            {"category": {"$regex": q, "$options": "i"}},
            {"brand": {"$regex": q, "$options": "i"}}
        ]
    }).limit(limit).to_list()
    
    # Extract unique suggestions
    unique_suggestions = set()
    for product in suggestions:
        # Add product name
        if q.lower() in product.name.lower():
            unique_suggestions.add(product.name)
        # Add category
        if q.lower() in product.category.lower():
            unique_suggestions.add(product.category)
        # Add brand
        if q.lower() in product.brand.lower():
            unique_suggestions.add(product.brand)
    
    return {"suggestions": list(unique_suggestions)[:limit]}