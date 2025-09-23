from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_search():
    response = client.get('/search?q=iPhone+15')
    assert response.status_code == 200
    data = response.json()
    assert 'product' in data
    assert 'offers' in data
    assert 'review_sentiments' in data

def test_create_alert():
    response = client.post('/alerts', json={"email": "test@example.com", "product": "iPhone 15", "price": 75000})
    assert response.status_code == 200
    assert response.json()["status"] == "success"
