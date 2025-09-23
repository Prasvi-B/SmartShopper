from fastapi import FastAPI
from alert_api import router as alert_router
from rate_limit import RateLimitMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()
app.add_middleware(RateLimitMiddleware, max_requests=10, window=60)
app.include_router(alert_router)

class Offer(BaseModel):
    site: str
    price: float
    url: str

class SearchResponse(BaseModel):
    product: str
    offers: List[Offer]
    review_sentiments: dict

@app.get("/search", response_model=SearchResponse)
def search(q: str):
    # Stub/mock data for MVP
    offers = [
        Offer(site="Amazon", price=79999, url="https://amazon.in/iphone15"),
        Offer(site="Flipkart", price=78999, url="https://flipkart.com/iphone15"),
        Offer(site="Myntra", price=80500, url="https://myntra.com/iphone15")
    ]
    review_sentiments = {"positive": 120, "negative": 30, "neutral": 50}
    return SearchResponse(product=q, offers=offers, review_sentiments=review_sentiments)
