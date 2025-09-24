"""
Simple baseline sentiment analysis model for Phase 1 MVP
Uses TextBlob for basic sentiment analysis - will be replaced with advanced models in Phase 3
"""

import joblib
from textblob import TextBlob
import numpy as np
from typing import List, Dict, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaselineSentimentAnalyzer:
    """
    Simple baseline sentiment analyzer using TextBlob
    This is a placeholder for Phase 1 - will be replaced with ML models later
    """
    
    def __init__(self):
        self.model_name = "textblob_baseline"
        self.version = "1.0.0"
    
    def predict_sentiment(self, text: str) -> Dict[str, float]:
        """
        Predict sentiment for a single text
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary with sentiment label and confidence score
        """
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity  # -1 to 1
            
            # Convert polarity to sentiment label
            if polarity > 0.1:
                label = "positive"
                confidence = min(polarity, 1.0)
            elif polarity < -0.1:
                label = "negative" 
                confidence = min(abs(polarity), 1.0)
            else:
                label = "neutral"
                confidence = 1.0 - abs(polarity)
            
            return {
                "text": text,
                "sentiment": label,
                "confidence": confidence,
                "polarity": polarity
            }
            
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
            return {
                "text": text,
                "sentiment": "neutral",
                "confidence": 0.5,
                "polarity": 0.0
            }
    
    def predict_batch(self, texts: List[str]) -> List[Dict[str, float]]:
        """
        Predict sentiment for multiple texts
        
        Args:
            texts: List of texts to analyze
            
        Returns:
            List of sentiment predictions
        """
        return [self.predict_sentiment(text) for text in texts]
    
    def get_summary_stats(self, predictions: List[Dict[str, float]]) -> Dict[str, int]:
        """
        Get summary statistics from predictions
        
        Args:
            predictions: List of sentiment predictions
            
        Returns:
            Dictionary with percentage breakdown
        """
        if not predictions:
            return {"positive": 0, "negative": 0, "neutral": 0}
        
        sentiment_counts = {"positive": 0, "negative": 0, "neutral": 0}
        
        for pred in predictions:
            sentiment_counts[pred["sentiment"]] += 1
        
        total = len(predictions)
        return {
            "positive": round((sentiment_counts["positive"] / total) * 100),
            "negative": round((sentiment_counts["negative"] / total) * 100),
            "neutral": round((sentiment_counts["neutral"] / total) * 100)
        }


# Global model instance
_model_instance = None

def get_model() -> BaselineSentimentAnalyzer:
    """Get or create model instance (singleton pattern)"""
    global _model_instance
    if _model_instance is None:
        _model_instance = BaselineSentimentAnalyzer()
        logger.info("Initialized baseline sentiment analyzer")
    return _model_instance


def analyze_review_sentiment(reviews: List[str]) -> Dict:
    """
    Analyze sentiment for a list of reviews
    
    Args:
        reviews: List of review texts
        
    Returns:
        Dictionary with predictions and summary
    """
    model = get_model()
    predictions = model.predict_batch(reviews)
    summary = model.get_summary_stats(predictions)
    
    return {
        "predictions": predictions,
        "summary": summary,
        "model_info": {
            "name": model.model_name,
            "version": model.version
        }
    }


if __name__ == "__main__":
    # Test the baseline model
    sample_reviews = [
        "This product is amazing! Great quality and fast delivery.",
        "Terrible quality, broke after one day. Very disappointed.",
        "It's okay, nothing special but does the job.",
        "Love it! Highly recommended for everyone.",
        "Worst purchase ever. Complete waste of money."
    ]
    
    result = analyze_review_sentiment(sample_reviews)
    
    print("Sentiment Analysis Results:")
    print(f"Summary: {result['summary']}")
    print(f"Model: {result['model_info']}")
    print("\nDetailed predictions:")
    for pred in result['predictions']:
        print(f"- {pred['sentiment'].upper()}: {pred['text'][:50]}... (confidence: {pred['confidence']:.2f})")