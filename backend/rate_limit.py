from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import time

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests=10, window=60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window = window
        self.clients = {}

    async def dispatch(self, request: Request, call_next):
        ip = request.client.host
        now = time.time()
        if ip not in self.clients:
            self.clients[ip] = []
        self.clients[ip] = [t for t in self.clients[ip] if now - t < self.window]
        if len(self.clients[ip]) >= self.max_requests:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        self.clients[ip].append(now)
        response = await call_next(request)
        return response
