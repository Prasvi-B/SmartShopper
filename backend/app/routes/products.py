from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from beanie import PydanticObjectId

from app.models.database import Product
from app.models.schemas import (
    ProductResponse, ProductCreate, ProductUpdate
)
from app.services.auth_service import get_current_user
from app.models.database import User

router = APIRouter()


@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: PydanticObjectId):
    """Get product details by ID"""
    product = await Product.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.get("/products", response_model=List[ProductResponse])
async def get_products(
    skip: int = 0,
    limit: int = 10,
    category: Optional[str] = None,
    brand: Optional[str] = None,
    search: Optional[str] = None
):
    """Get products with optional filtering"""
    query = {}
    
    if category:
        query["category"] = category
    if brand:
        query["brand"] = brand
    
    if search:
        # Text search
        products = await Product.find(
            {"$text": {"$search": search}},
            query
        ).skip(skip).limit(limit).to_list()
    else:
        products = await Product.find(query).skip(skip).limit(limit).to_list()
    
    return products


@router.post("/products", response_model=ProductResponse)
async def create_product(
    product_data: ProductCreate,
    current_user: User = Depends(get_current_user)
):
    """Create a new product (admin only)"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403, 
            detail="Not enough permissions to create products"
        )
    
    # Create new product
    product = Product(**product_data.model_dump())
    await product.insert()
    return product


@router.put("/products/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: PydanticObjectId,
    product_data: ProductUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update a product (admin only)"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403, 
            detail="Not enough permissions to update products"
        )
    
    product = await Product.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Update product
    update_data = product_data.model_dump(exclude_unset=True)
    await product.update({"$set": update_data})
    
    return await Product.get(product_id)


@router.delete("/products/{product_id}")
async def delete_product(
    product_id: PydanticObjectId,
    current_user: User = Depends(get_current_user)
):
    """Delete a product (admin only)"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403, 
            detail="Not enough permissions to delete products"
        )
    
    product = await Product.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    await product.delete()
    return {"message": "Product deleted successfully"}