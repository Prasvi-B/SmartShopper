# Scraper service Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install scrapy requests beautifulsoup4
CMD ["scrapy", "crawl", "default"]
