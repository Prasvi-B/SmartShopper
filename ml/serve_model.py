from fastapi import FastAPI
from pydantic import BaseModel
import joblib
from transformers import pipeline

app = FastAPI()

class SentimentRequest(BaseModel):
    texts: list

class SentimentResponse(BaseModel):
    results: list

# Load baseline model
vectorizer = joblib.load('tfidf_vectorizer.joblib')
clf = joblib.load('sentiment_model.joblib')

# Load transformer pipeline
transformer_pipe = pipeline('sentiment-analysis', model='transformer_sentiment_model', tokenizer='transformer_sentiment_model')

@app.post('/predict_baseline', response_model=SentimentResponse)
def predict_baseline(req: SentimentRequest):
    X = vectorizer.transform(req.texts)
    preds = clf.predict(X)
    return SentimentResponse(results=preds.tolist())

@app.post('/predict_transformer', response_model=SentimentResponse)
def predict_transformer(req: SentimentRequest):
    results = transformer_pipe(req.texts)
    sentiments = [r['label'] for r in results]
    return SentimentResponse(results=sentiments)
