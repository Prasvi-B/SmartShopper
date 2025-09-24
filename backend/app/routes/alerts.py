from fastapi import APIRouter, Depends, HTTPException
from typing import List
from beanie import PydanticObjectId

from app.models.database import PriceAlert, Product, User
from app.models.schemas import (
    PriceAlertResponse, PriceAlertCreate, PriceAlertUpdate
)
from app.services.auth_service import get_current_user

router = APIRouter()


@router.post("/alerts", response_model=PriceAlertResponse)
async def create_price_alert(
    alert_data: PriceAlertCreate,
    current_user: User = Depends(get_current_user)
):
    """Create a new price alert"""
    # Verify product exists
    product = await Product.get(alert_data.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if user already has an alert for this product
    existing_alert = await PriceAlert.find_one({
        "product_id": alert_data.product_id,
        "user_id": current_user.id,
        "is_active": True
    })
    if existing_alert:
        raise HTTPException(
            status_code=400, 
            detail="You already have an active alert for this product"
        )
    
    # Create new price alert
    alert = PriceAlert(
        **alert_data.model_dump(),
        user_id=current_user.id,
        product_name=product.name,
        current_price=product.price
    )
    await alert.insert()
    return alert


@router.get("/alerts", response_model=List[PriceAlertResponse])
async def get_user_alerts(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user)
):
    """Get all alerts for the current user"""
    alerts = await PriceAlert.find(
        {"user_id": current_user.id}
    ).sort("-created_at").skip(skip).limit(limit).to_list()
    return alerts


@router.get("/alerts/{alert_id}", response_model=PriceAlertResponse)
async def get_price_alert(
    alert_id: PydanticObjectId,
    current_user: User = Depends(get_current_user)
):
    """Get a specific price alert"""
    alert = await PriceAlert.get(alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Price alert not found")
    
    # Check if the alert belongs to the current user
    if alert.user_id != current_user.id:
        raise HTTPException(
            status_code=403, 
            detail="Not enough permissions to view this alert"
        )
    
    return alert


@router.put("/alerts/{alert_id}", response_model=PriceAlertResponse)
async def update_price_alert(
    alert_id: PydanticObjectId,
    alert_data: PriceAlertUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update a price alert"""
    alert = await PriceAlert.get(alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Price alert not found")
    
    # Check if the alert belongs to the current user
    if alert.user_id != current_user.id:
        raise HTTPException(
            status_code=403, 
            detail="Not enough permissions to update this alert"
        )
    
    # Update alert
    update_data = alert_data.model_dump(exclude_unset=True)
    await alert.update({"$set": update_data})
    
    return await PriceAlert.get(alert_id)


@router.delete("/alerts/{alert_id}")
async def delete_price_alert(
    alert_id: PydanticObjectId,
    current_user: User = Depends(get_current_user)
):
    """Delete a price alert"""
    alert = await PriceAlert.get(alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Price alert not found")
    
    # Check if the alert belongs to the current user
    if alert.user_id != current_user.id:
        raise HTTPException(
            status_code=403, 
            detail="Not enough permissions to delete this alert"
        )
    
    await alert.delete()
    return {"message": "Price alert deleted successfully"}