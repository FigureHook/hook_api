from fastapi import APIRouter

from .endpoints import products, webhooks, company, series

api_router = APIRouter()

api_router.include_router(
    products.router, prefix='/products', tags=['product']
)
api_router.include_router(
    webhooks.router, prefix='/webhooks', tags=['webhook']
)
api_router.include_router(
    company.router, prefix='/companys', tags=['compnay']
)
api_router.include_router(
    series.router, prefix='/series', tags=['series']
)
