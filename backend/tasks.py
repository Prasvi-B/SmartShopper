from celery import Celery
from scrapers.amazon_scraper import search_amazon
from scrapers.flipkart_scraper import search_flipkart
from scrapers.review_scraper import scrape_reviews_amazon, scrape_reviews_flipkart

celery_app = Celery('tasks', broker='redis://localhost:6379/0')

@celery_app.task
def periodic_scrape(query):
    amazon_results = search_amazon(query)
    flipkart_results = search_flipkart(query)
    # Save results to DB (omitted for brevity)
    return {'amazon': amazon_results, 'flipkart': flipkart_results}

@celery_app.task
def check_price_alerts():
    # Query DB for active alerts, check current prices, send emails if triggered (omitted for brevity)
    pass

@celery_app.task
def retrain_sentiment_model():
    # Trigger ML pipeline for retraining (omitted for brevity)
    pass
