from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware

from .api.v1.api import api_router
from .core.config import settings

app = FastAPI(
    title="FigureHook",
    version="0.0.1",
    debug=settings.DEBUG,
)


app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(CorrelationIdMiddleware)
app.include_router(api_router, prefix=settings.API_V1_ENDPOINT)
