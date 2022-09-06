import logging

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from sqlalchemy.exc import SQLAlchemyError

from .api.v1.api import api_router
from .core.config import settings
from .core.logging import configure_logging
from .handlers.exception_handlers import sqlalchemy_exception_handler

app = FastAPI(
    title="FigureHook",
    version="0.0.1",
    debug=settings.DEBUG,
    on_startup=[configure_logging]
)

app.add_middleware(GZipMiddleware)
app.add_middleware(CorrelationIdMiddleware)

app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)

app.include_router(api_router, prefix=settings.API_V1_ENDPOINT)


if settings.ENVIRONMENT == 'development':
    console_logger = logging.getLogger('uvicorn')
    console_logger.info(f"Token: {str(settings.API_TOKEN)}")
