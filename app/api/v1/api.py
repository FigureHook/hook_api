from fastapi import APIRouter

from .endpoints import products, webhooks

api_router = APIRouter()

api_router.include_router(
    products.router, prefix="/products", tags=['product'])
api_router.include_router(
    webhooks.router, prefix="/webhooks", tags=['webhook']
)
