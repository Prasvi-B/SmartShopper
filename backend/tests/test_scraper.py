from services.scraper import get_prices

def test_get_prices():
    prices = get_prices('iPhone 15')
    assert isinstance(prices, list)
    assert len(prices) > 0
