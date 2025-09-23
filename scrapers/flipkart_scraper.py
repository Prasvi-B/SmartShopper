import requests
from bs4 import BeautifulSoup
from typing import List, Dict

def search_flipkart(query: str) -> List[Dict]:
    url = f"https://www.flipkart.com/search?q={query.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    results = []
    for item in soup.select('._1AtVbE'):
        title = item.select_one('._4rR01T')
        price = item.select_one('._30jeq3')
        link = item.select_one('a._1fQZEK')
        if title and price and link:
            results.append({
                'site': 'Flipkart',
                'product_title': title.text.strip(),
                'price': float(price.text.replace('₹', '').replace(',', '')),  # INR
                'currency': 'INR',
                'url': f"https://www.flipkart.com{link['href']}",
                'timestamp': None
            })
    return results
