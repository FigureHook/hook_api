import logging

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware

from .api.v1.api import api_router
from .core.config import settings
from .core.logging import configure_logging

logger = logging.getLogger(__name__)

app = FastAPI(
    title="FigureHook",
    version="0.0.1",
    debug=settings.DEBUG,
    on_startup=[configure_logging]
)

app.add_middleware(GZipMiddleware)
app.add_middleware(CorrelationIdMiddleware)

app.include_router(api_router, prefix=settings.API_V1_ENDPOINT)

if settings.ENVIRONMENT == 'development':
    logger = logging.getLogger('uvicorn')
    logger.info(f"Token: {settings.API_TOKEN}")
