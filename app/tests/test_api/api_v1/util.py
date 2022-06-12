from app.core.config import settings


def v1_endpoint(path: str):
    return f"{settings.API_V1_ENDPOINT}{path}"
