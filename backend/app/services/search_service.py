from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.database import Product, Offer, Review
from app.models.schemas import SearchQuery, SearchResponse, ProductSummary
import asyncio


class SearchService:
    def __init__(self, db: Session):
        self.db = db
    
    async def search_products(
        self, 
        search_query: SearchQuery, 
        limit: int = 20, 
        offset: int = 0
    ) -> SearchResponse:
        """
        Search for products based on query parameters
        Currently returns mock data - will be replaced with real scraping in Phase 2
        """
        # Mock data for Phase 1 MVP
        mock_products = [
            {
                "id": 1,
                "name": "iPhone 15 Pro",
                "description": "Latest Apple iPhone with A17 Pro chip",
                "brand": "Apple",
                "image_url": "https://example.com/iphone15.jpg",
                "min_price": 128900.0,
                "max_price": 159900.0,
                "avg_rating": 4.5,
                "total_reviews": 1250,
                "best_offer": {
                    "id": 1,
                    "platform": "amazon",
                    "url": "https://amazon.in/iphone15pro",
                    "price": 128900.0,
                    "original_price": 134900.0,
                    "discount_percentage": 4.5,
                    "availability": "in_stock",
                    "seller_name": "Amazon",
                    "shipping_cost": 0.0
                },
                "sentiment_summary": {
                    "positive": 65,
                    "negative": 15,
                    "neutral": 20,
                    "avg_sentiment": 0.6
                }
            },
            {
                "id": 2,
                "name": "Samsung Galaxy S24 Ultra",
                "description": "Premium Android flagship with S Pen",
                "brand": "Samsung",
                "image_url": "https://example.com/galaxy-s24.jpg",
                "min_price": 124999.0,
                "max_price": 134999.0,
                "avg_rating": 4.3,
                "total_reviews": 890,
                "best_offer": {
                    "id": 2,
                    "platform": "flipkart",
                    "url": "https://flipkart.com/galaxy-s24-ultra",
                    "price": 124999.0,
                    "original_price": 129999.0,
                    "discount_percentage": 3.8,
                    "availability": "in_stock",
                    "seller_name": "Flipkart",
                    "shipping_cost": 0.0
                },
                "sentiment_summary": {
                    "positive": 58,
                    "negative": 22,
                    "neutral": 20,
                    "avg_sentiment": 0.4
                }
            }
        ]
        
        # Filter mock data based on query (simple implementation)
        filtered_products = []
        for product in mock_products:
            if search_query.query.lower() in product["name"].lower():
                if search_query.min_price and product["min_price"] < search_query.min_price:
                    continue
                if search_query.max_price and product["max_price"] > search_query.max_price:
                    continue
                filtered_products.append(product)
        
        # Apply pagination
        paginated_products = filtered_products[offset:offset + limit]
        
        return SearchResponse(
            products=paginated_products,
            total_count=len(filtered_products),
            query=search_query.query
        )
    
    async def get_suggestions(self, query: str, limit: int = 10) -> List[str]:
        """
        Get autocomplete suggestions for search queries
        """
        # Mock suggestions for Phase 1
        mock_suggestions = [
            "iPhone 15",
            "iPhone 15 Pro",
            "iPhone 15 Pro Max",
            "Samsung Galaxy S24",
            "Samsung Galaxy S24 Ultra",
            "MacBook Pro",
            "MacBook Air",
            "AirPods Pro",
            "iPad Pro",
            "Apple Watch"
        ]
        
        # Simple filtering based on query
        suggestions = [
            suggestion for suggestion in mock_suggestions
            if query.lower() in suggestion.lower()
        ]
        
        return suggestions[:limit]