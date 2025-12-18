from fastapi import FastAPI
import logging

logger = logging.getLogger("uvicorn.error")

try:
    # Import the real application from main.py in the same directory
    from main import app as real_app
    app = real_app
except Exception as e:
    # If import fails (missing deps / runtime error), expose a lightweight fallback app
    logger.exception("Failed to import backend application: %s", e)

    fallback = FastAPI(title="Fallback Backend")

    @fallback.get("/")
    async def root():
        return {"error": "backend import failed", "detail": str(e)}

    @fallback.get("/health")
    async def health():
        return {"status": "degraded", "detail": "backend import failed"}

    app = fallback
