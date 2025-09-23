# ML service Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install scikit-learn joblib transformers datasets
CMD ["python", "serve_model.py"]
