"""
FastAPI application — the target app for the CI/CD pipeline demo.
Provides a simple but real API with health, metrics, and crypto endpoints.
"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import time
import platform

app = FastAPI(
    title="Crypto API",
    description="Demo app for CI/CD pipeline — live crypto prices endpoint",
    version="1.0.0",
)

START_TIME = time.time()


@app.get("/")
def root():
    return {"message": "Crypto API is running", "docs": "/docs"}


@app.get("/health")
def health():
    """Health check endpoint — used by deployment platform."""
    return {
        "status": "healthy",
        "uptime_seconds": round(time.time() - START_TIME, 2),
        "python": platform.python_version(),
    }


@app.get("/metrics")
def metrics():
    """Basic runtime metrics."""
    return {
        "uptime_seconds": round(time.time() - START_TIME, 2),
        "platform": platform.system(),
        "python_version": platform.python_version(),
    }


@app.get("/coins")
def list_coins():
    """Returns the list of tracked coins."""
    return {
        "coins": ["bitcoin", "ethereum", "solana", "cardano", "polkadot"],
        "count": 5,
    }


@app.get("/coins/{coin_id}")
def get_coin(coin_id: str):
    """Returns info for a specific coin."""
    valid = {"bitcoin", "ethereum", "solana", "cardano", "polkadot"}
    if coin_id not in valid:
        raise HTTPException(status_code=404, detail=f"Coin '{coin_id}' not tracked")
    return {"coin_id": coin_id, "tracked": True}
