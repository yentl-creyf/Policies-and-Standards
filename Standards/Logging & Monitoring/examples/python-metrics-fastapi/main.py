from fastapi import FastAPI, Request
from prometheus_client import make_asgi_app, Counter, Histogram
from starlette.middleware.base import BaseHTTPMiddleware
import time

# Create FastAPI app
app = FastAPI()

# Define Prometheus metrics
REQUEST_COUNT = Counter(
    "request_count", "Total number of requests", ["method", "endpoint", "http_status"]
)
REQUEST_LATENCY = Histogram(
    "request_latency_seconds", "Latency of requests in seconds", ["endpoint"]
)

# Create ASGI app for Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Middleware for Prometheus metrics logging
class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Start timer for request latency
        start_time = time.time()

        # Process request
        response = await call_next(request)

        # Calculate request latency
        request_latency = time.time() - start_time
        endpoint = request.url.path

        # Update Prometheus metrics
        REQUEST_COUNT.labels(method=request.method, endpoint=endpoint, http_status=response.status_code).inc()
        REQUEST_LATENCY.labels(endpoint=endpoint).observe(request_latency)

        return response

# Add Prometheus middleware to app
app.add_middleware(PrometheusMiddleware)

# Define a sample route
@app.get("/")
async def read_root():
    return {"message": "Hello, world!"}