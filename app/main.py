from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

from .api.api_v1.api import api_router

app = FastAPI(
    title="FigureHook",
    version="v0.0.1",
    openapi_url="/v1/openapi.json"
)

app.include_router(api_router, prefix="/v1")
