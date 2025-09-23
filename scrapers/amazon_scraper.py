import requests
from bs4 import BeautifulSoup
from typing import List, Dict

def search_amazon(query: str) -> List[Dict]:
    url = f"https://www.amazon.in/s?k={query.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    results = []
    for item in soup.select('.s-result-item'):
        title = item.select_one('h2 span')
        price = item.select_one('.a-price-whole')
        link = item.select_one('a.a-link-normal')
        if title and price and link:
            results.append({
                'site': 'Amazon',
                'product_title': title.text.strip(),
                'price': float(price.text.replace(',', '')),  # INR
                'currency': 'INR',
                'url': f"https://www.amazon.in{link['href']}",
                'timestamp': None
            })
    return results
