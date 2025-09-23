import pandas as pd
import glob
import os

def build_review_dataset(scraped_dir='scraped_reviews/'):
    files = glob.glob(os.path.join(scraped_dir, '*.csv'))
    dfs = [pd.read_csv(f) for f in files]
    df = pd.concat(dfs, ignore_index=True)
    # Weak supervision: infer sentiment from rating
    def infer_sentiment(rating):
        if rating >= 4:
            return 'positive'
        elif rating <= 2:
            return 'negative'
        else:
            return 'neutral'
    df['sentiment'] = df['rating'].apply(infer_sentiment)
    df = df[['text', 'sentiment']]
    df.to_csv('review_dataset.csv', index=False)
    print('Dataset built:', df.shape)

if __name__ == '__main__':
    build_review_dataset()
