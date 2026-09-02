"""
Demonstrates Settings, CORS, and a custom logging middleware together.
"""

import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings

app = FastAPI(
    title="Learning FastAPI",
    description="Configuration, middlewares and deploy example",
    version="0.1.0",
)

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Custom logging middleware ---
@app.middleware("http")
async def log_requests(request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    elapsed = time.perf_counter() - start
    print(f"{request.method} {request.url.path} -> {elapsed:.3f}s")
    return response


@app.get("/")
def read_root():
    return {"message": "Configured via environment variables"}


@app.get("/config-check")
def config_check():
    """
    Proves the settings were actually loaded from .env -- never
    expose the real secret_key like this in a real project, this
    endpoint exists ONLY to demonstrate that config loading works.
    """
    return {
        "algorithm": settings.algorithm,
        "access_token_expire_minutes": settings.access_token_expire_minutes,
        "secret_key_loaded": bool(settings.secret_key),
    }
