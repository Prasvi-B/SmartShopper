"""
Product routes for search and product management
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from beanie import PydanticObjectId

from app.models.schemas import (
    ProductCreate, Product as ProductSchema, SearchQuery, SearchResponse,
    ProductSummary, Offer as OfferSchema
)
from app.models.mongodb_models import Product, Offer, Review
from app.services.auth_service import get_current_user_optional, get_current_active_user
from app.models.mongodb_models import User

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/search", response_model=SearchResponse)
async def search_products(
    query: str = Query(..., min_length=1),
    category: Optional[str] = None,
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    platform: Optional[str] = None,
    limit: int = Query(20, ge=1, le=100),
    skip: int = Query(0, ge=0),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Search for products with filters"""
    # Build search query
    search_filter = {"$text": {"$search": query}}
    
    if category:
        search_filter["category"] = {"$regex": category, "$options": "i"}
    
    # Find matching products
    products = await Product.find(search_filter).skip(skip).limit(limit).to_list()
    
    # Get product summaries with offers and reviews
    product_summaries = []
    for product in products:
        # Get offers for this product
        offers = await Offer.find({"product_id": product.id}).to_list()
        
        # Filter by price range
        if min_price is not None:
            offers = [offer for offer in offers if offer.price >= min_price]
        if max_price is not None:
            offers = [offer for offer in offers if offer.price <= max_price]
        
        if not offers:
            continue
        
        # Filter by platform
        if platform:
            offers = [offer for offer in offers if offer.platform.value == platform]
            if not offers:
                continue
        
        # Calculate price range
        prices = [offer.price for offer in offers]
        min_price_val = min(prices) if prices else 0
        max_price_val = max(prices) if prices else 0
        
        # Get best offer (lowest price)
        best_offer = min(offers, key=lambda x: x.price) if offers else None
        
        # Get reviews and ratings
        reviews = await Review.find({"product_id": product.id}).to_list()
        avg_rating = sum(review.rating for review in reviews) / len(reviews) if reviews else 0
        
        # Create sentiment summary
        sentiment_counts = {"positive": 0, "negative": 0, "neutral": 0}
        for review in reviews:
            if review.sentiment_label:
                sentiment_counts[review.sentiment_label] += 1
        
        product_summary = ProductSummary(
            id=str(product.id),
            name=product.name,
            description=product.description,
            brand=product.brand,
            image_url=product.image_url,
            min_price=min_price_val,
            max_price=max_price_val,
            avg_rating=round(avg_rating, 2),
            total_reviews=len(reviews),
            best_offer=OfferSchema(
                id=str(best_offer.id),
                product_id=str(best_offer.product_id),
                platform=best_offer.platform,
                url=best_offer.url,
                price=best_offer.price,
                original_price=best_offer.original_price,
                discount_percentage=best_offer.discount_percentage,
                availability=best_offer.availability,
                seller_name=best_offer.seller_name,
                shipping_cost=best_offer.shipping_cost,
                created_at=best_offer.created_at,
                updated_at=best_offer.updated_at
            ) if best_offer else None,
            sentiment_summary=sentiment_counts
        )
        
        product_summaries.append(product_summary)
    
    # Save search to history if user is logged in
    if current_user:
        from app.models.mongodb_models import SearchHistory
        from datetime import datetime, timezone
        
        search_history = SearchHistory(
            user_id=current_user.id,
            query=query,
            results_count=len(product_summaries)
        )
        await search_history.insert()
    
    return SearchResponse(
        products=product_summaries,
        total_count=len(product_summaries),
        query=query
    )


@router.get("/{product_id}", response_model=ProductSchema)
async def get_product(product_id: str):
    """Get product details by ID"""
    try:
        product = await Product.get(PydanticObjectId(product_id))
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        
        return ProductSchema(
            id=str(product.id),
            name=product.name,
            description=product.description,
            category=product.category,
            brand=product.brand,
            image_url=product.image_url,
            created_at=product.created_at,
            updated_at=product.updated_at
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid product ID"
        )


@router.get("/{product_id}/offers", response_model=List[OfferSchema])
async def get_product_offers(product_id: str):
    """Get all offers for a product"""
    try:
        product_obj_id = PydanticObjectId(product_id)
        
        # Verify product exists
        product = await Product.get(product_obj_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        
        # Get offers
        offers = await Offer.find({"product_id": product_obj_id}).to_list()
        
        return [
            OfferSchema(
                id=str(offer.id),
                product_id=str(offer.product_id),
                platform=offer.platform,
                url=offer.url,
                price=offer.price,
                original_price=offer.original_price,
                discount_percentage=offer.discount_percentage,
                availability=offer.availability,
                seller_name=offer.seller_name,
                shipping_cost=offer.shipping_cost,
                created_at=offer.created_at,
                updated_at=offer.updated_at
            )
            for offer in offers
        ]
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid product ID"
        )


@router.post("/", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Create a new product (authenticated users only)"""
    product = Product(
        name=product_data.name,
        description=product_data.description,
        category=product_data.category,
        brand=product_data.brand,
        image_url=product_data.image_url
    )
    
    await product.insert()
    
    return ProductSchema(
        id=str(product.id),
        name=product.name,
        description=product.description,
        category=product.category,
        brand=product.brand,
        image_url=product.image_url,
        created_at=product.created_at,
        updated_at=product.updated_at
    )
