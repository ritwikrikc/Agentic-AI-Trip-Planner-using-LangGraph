from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
from importlib import import_module

# Create the FastAPI app and configure CORS and logging for cloud deployments
app = FastAPI(title="Agentic AI Trip Planner", version="0.1.0")

# Simple, permissive CORS defaults suitable for many cloud deployments.
# Adjust origins in production as needed.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("CORS_ALLOW_ORIGIN", "*")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Import and include routes from the `routes` module. Import done here so the
# module import errors are raised at startup time rather than at top-level
# (gives clearer behavior when deploying).
try:
    routes_mod = import_module("routes")
    if hasattr(routes_mod, "router"):
        app.include_router(routes_mod.router)
    else:
        logger.warning("Module 'routes' imported but no 'router' attribute found.")
except Exception as e:
    logger.exception("Failed to import routes module: %s", e)


if __name__ == "__main__":
    # Lightweight run guard for local testing. Cloud deployments should run
    # the app with a production ASGI server (uvicorn/gunicorn) instead.
    import uvicorn

    # Control the reload behavior with an environment variable.
    # Set UVICORN_RELOAD=1 or UVICORN_RELOAD=true for development convenience.
    reload_flag = os.getenv("UVICORN_RELOAD", "false").lower() in ("1", "true", "yes")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=reload_flag,
    )
    