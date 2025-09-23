from services.sentiment import analyze_sentiment

def test_analyze_sentiment():
    sentiments = analyze_sentiment('iPhone 15')
    assert 'positive' in sentiments
    assert 'negative' in sentiments
    assert 'neutral' in sentiments
