from rapidfuzz import fuzz

def normalize_title(title: str) -> str:
    return title.lower().replace(' ', '').replace('-', '').replace('_', '')

def match_titles(title1: str, title2: str) -> bool:
    return fuzz.ratio(normalize_title(title1), normalize_title(title2)) > 80

def normalize_price(price: float, currency: str, to_currency: str = 'INR') -> float:
    # For demo, assume 1:1 conversion
    return price
