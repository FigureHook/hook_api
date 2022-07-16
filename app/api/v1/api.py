from fastapi import APIRouter

from .endpoints import (category, company, paintwork, products, sculptor,
                        series, webhooks)

api_router = APIRouter()

api_router.include_router(
    products.router, prefix='/products', tags=['product'])
api_router.include_router(
    webhooks.router, prefix='/webhooks', tags=['webhook'])
api_router.include_router(
    company.router, prefix='/companys', tags=['compnay'])
api_router.include_router(
    series.router, prefix='/series', tags=['series'])
api_router.include_router(
    category.router, prefix='/categories', tags=['category'])
api_router.include_router(
    sculptor.router, prefix='/sculptors', tags=['sculptor', 'worker'])
api_router.include_router(
    paintwork.router, prefix='/paintworks', tags=['paintwork', 'worker'])
