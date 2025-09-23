# ML Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY ml/ .
RUN pip install scikit-learn joblib transformers datasets fastapi uvicorn
CMD ["python", "serve_model.py"]
