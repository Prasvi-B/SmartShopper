import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

df = pd.read_csv('review_dataset_clean.csv')
X = df['text']
y = df['sentiment']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
vectorizer = TfidfVectorizer(max_features=5000)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)
clf = LogisticRegression(max_iter=1000)
clf.fit(X_train_vec, y_train)
preds = clf.predict(X_test_vec)
print(classification_report(y_test, preds))
joblib.dump(vectorizer, 'tfidf_vectorizer.joblib')
joblib.dump(clf, 'sentiment_model.joblib')
