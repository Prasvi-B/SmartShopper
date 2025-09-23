import requests
from bs4 import BeautifulSoup
from typing import List, Dict

def scrape_reviews_amazon(product_url: str) -> List[Dict]:
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(product_url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    reviews = []
    for item in soup.select('.review'):  # Simplified selector
        text = item.select_one('.review-text')
        rating = item.select_one('.review-rating')
        if text and rating:
            reviews.append({
                'source': 'Amazon',
                'text': text.text.strip(),
                'rating': float(rating.text[0]),
                'timestamp': None
            })
    return reviews

def scrape_reviews_flipkart(product_url: str) -> List[Dict]:
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(product_url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    reviews = []
    for item in soup.select('._16PBlm'):
        text = item.select_one('._6K-7Co')
        rating = item.select_one('._3LWZlK')
        if text and rating:
            reviews.append({
                'source': 'Flipkart',
                'text': text.text.strip(),
                'rating': float(rating.text),
                'timestamp': None
            })
    return reviews
