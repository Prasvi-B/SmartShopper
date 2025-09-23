import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

stop_words = set(stopwords.words('english'))

def clean_text(text):
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)
    text = text.lower()
    tokens = word_tokenize(text)
    tokens = [w for w in tokens if w not in stop_words]
    return ' '.join(tokens)

def preprocess_dataset(input_csv='review_dataset.csv', output_csv='review_dataset_clean.csv'):
    df = pd.read_csv(input_csv)
    df['text'] = df['text'].apply(clean_text)
    df.to_csv(output_csv, index=False)
    print('Preprocessed:', df.shape)

if __name__ == '__main__':
    preprocess_dataset()
