"""
User feature routes for wishlists, price alerts, and search history
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime, timezone

from app.models.schemas import (
    WishlistItemCreate, WishlistItem, PriceAlertCreate, PriceAlert,
    SearchHistoryItem
)
from app.services.auth_service import get_current_active_user, get_current_user_optional
from app.models.mongodb_models import User, Wishlist, PriceAlert as PriceAlertModel, SearchHistory

router = APIRouter(prefix="/user", tags=["user_features"])


# Wishlist endpoints
@router.post("/wishlist", response_model=WishlistItem, status_code=status.HTTP_201_CREATED)
async def add_to_wishlist(
    item: WishlistItemCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Add product to user's wishlist"""
    # Check if item already exists in wishlist
    existing_item = await Wishlist.find_one({
        "user_id": current_user.id,
        "product_id": item.product_id
    })
    
    if existing_item:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product already in wishlist"
        )
    
    # Create new wishlist item
    wishlist_item = Wishlist(
        user_id=current_user.id,
        product_id=item.product_id
    )
    
    await wishlist_item.insert()
    
    return WishlistItem(
        id=str(wishlist_item.id),
        product_id=wishlist_item.product_id,
        user_id=str(wishlist_item.user_id),
        created_at=wishlist_item.created_at
    )


@router.get("/wishlist", response_model=List[WishlistItem])
async def get_user_wishlist(
    current_user: User = Depends(get_current_active_user)
):
    """Get user's wishlist"""
    wishlist_items = await Wishlist.find({"user_id": current_user.id}).to_list()
    
    return [
        WishlistItem(
            id=str(item.id),
            product_id=item.product_id,
            user_id=str(item.user_id),
            created_at=item.created_at
        )
        for item in wishlist_items
    ]


@router.delete("/wishlist/{product_id}")
async def remove_from_wishlist(
    product_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Remove product from user's wishlist"""
    wishlist_item = await Wishlist.find_one({
        "user_id": current_user.id,
        "product_id": product_id
    })
    
    if not wishlist_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found in wishlist"
        )
    
    await wishlist_item.delete()
    return {"message": "Product removed from wishlist"}


# Price Alert endpoints
@router.post("/alerts", response_model=PriceAlert, status_code=status.HTTP_201_CREATED)
async def create_price_alert(
    alert: PriceAlertCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Create a price alert for a product"""
    # Check if alert already exists for this user and product
    existing_alert = await PriceAlertModel.find_one({
        "user_id": current_user.id,
        "product_id": alert.product_id,
        "is_active": True
    })
    
    if existing_alert:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Active price alert already exists for this product"
        )
    
    # Create new price alert
    price_alert = PriceAlertModel(
        user_id=current_user.id,
        product_id=alert.product_id,
        target_price=alert.target_price,
        is_active=True
    )
    
    await price_alert.insert()
    
    return PriceAlert(
        id=str(price_alert.id),
        product_id=price_alert.product_id,
        user_id=str(price_alert.user_id),
        target_price=price_alert.target_price,
        is_active=price_alert.is_active,
        created_at=price_alert.created_at,
        last_checked=price_alert.last_checked
    )


@router.get("/alerts", response_model=List[PriceAlert])
async def get_user_price_alerts(
    active_only: bool = True,
    current_user: User = Depends(get_current_active_user)
):
    """Get user's price alerts"""
    query = {"user_id": current_user.id}
    if active_only:
        query["is_active"] = True
    
    alerts = await PriceAlertModel.find(query).to_list()
    
    return [
        PriceAlert(
            id=str(alert.id),
            product_id=alert.product_id,
            user_id=str(alert.user_id),
            target_price=alert.target_price,
            is_active=alert.is_active,
            created_at=alert.created_at,
            last_checked=alert.last_checked
        )
        for alert in alerts
    ]


@router.patch("/alerts/{alert_id}")
async def update_price_alert(
    alert_id: str,
    target_price: Optional[float] = None,
    is_active: Optional[bool] = None,
    current_user: User = Depends(get_current_active_user)
):
    """Update a price alert"""
    alert = await PriceAlertModel.find_one({
        "id": alert_id,
        "user_id": current_user.id
    })
    
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Price alert not found"
        )
    
    # Update fields
    if target_price is not None:
        alert.target_price = target_price
    if is_active is not None:
        alert.is_active = is_active
    
    alert.updated_at = datetime.now(timezone.utc)
    await alert.save()
    
    return {"message": "Price alert updated successfully"}


@router.delete("/alerts/{alert_id}")
async def delete_price_alert(
    alert_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Delete a price alert"""
    alert = await PriceAlertModel.find_one({
        "id": alert_id,
        "user_id": current_user.id
    })
    
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Price alert not found"
        )
    
    await alert.delete()
    return {"message": "Price alert deleted successfully"}


# Search History endpoints
@router.get("/search-history", response_model=List[SearchHistoryItem])
async def get_search_history(
    limit: int = 50,
    current_user: User = Depends(get_current_active_user)
):
    """Get user's search history"""
    history = await SearchHistory.find(
        {"user_id": current_user.id}
    ).sort([("created_at", -1)]).limit(limit).to_list()
    
    return [
        SearchHistoryItem(
            id=str(item.id),
            user_id=str(item.user_id),
            query=item.query,
            results_count=item.results_count,
            created_at=item.created_at
        )
        for item in history
    ]


@router.post("/search-history")
async def add_search_to_history(
    query: str,
    results_count: int,
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Add search query to user's history (if logged in)"""
    if not current_user:
        return {"message": "Search not saved - user not logged in"}
    
    # Check if the same query was searched recently (within last hour)
    recent_search = await SearchHistory.find_one({
        "user_id": current_user.id,
        "query": query,
        "created_at": {"$gte": datetime.now(timezone.utc).replace(hour=datetime.now(timezone.utc).hour-1)}
    })
    
    if not recent_search:
        # Add new search history entry
        search_history = SearchHistory(
            user_id=current_user.id,
            query=query,
            results_count=results_count
        )
        await search_history.insert()
    
    return {"message": "Search added to history"}


@router.delete("/search-history/{search_id}")
async def delete_search_history_item(
    search_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Delete a search history item"""
    search_item = await SearchHistory.find_one({
        "id": search_id,
        "user_id": current_user.id
    })
    
    if not search_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Search history item not found"
        )
    
    await search_item.delete()
    return {"message": "Search history item deleted"}


@router.delete("/search-history")
async def clear_search_history(
    current_user: User = Depends(get_current_active_user)
):
    """Clear all search history for user"""
    await SearchHistory.find({"user_id": current_user.id}).delete()
    return {"message": "Search history cleared"}


# Dashboard/Stats endpoints
@router.get("/dashboard/stats")
async def get_user_dashboard_stats(
    current_user: User = Depends(get_current_active_user)
):
    """Get user dashboard statistics"""
    # Count user's data
    wishlist_count = await Wishlist.find({"user_id": current_user.id}).count()
    active_alerts_count = await PriceAlertModel.find({
        "user_id": current_user.id, 
        "is_active": True
    }).count()
    search_history_count = await SearchHistory.find({"user_id": current_user.id}).count()
    
    # Get recent search queries
    recent_searches = await SearchHistory.find(
        {"user_id": current_user.id}
    ).sort([("created_at", -1)]).limit(5).to_list()
    
    return {
        "wishlist_count": wishlist_count,
        "active_alerts_count": active_alerts_count,
        "search_history_count": search_history_count,
        "recent_searches": [
            {
                "query": search.query,
                "results_count": search.results_count,
                "created_at": search.created_at
            }
            for search in recent_searches
        ]
    }