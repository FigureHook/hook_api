from .core.config import settings
from .api.v1.api import api_router
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()


app = FastAPI(
    title="FigureHook",
    version="v0.0.1",
    openapi_url=f"{settings.API_V1_ENDPOINT}/openapi.json"
)

app.include_router(api_router, prefix=settings.API_V1_ENDPOINT)
