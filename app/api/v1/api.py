from app.api import deps
from fastapi import APIRouter, Depends, Response

from .endpoints import (application, category, company, paintwork, products,
                        sculptor, series, source_checksum, webhooks)

api_router = APIRouter(dependencies=[Depends(deps.verify_token)])

api_router.include_router(
    products.router, prefix='/products', tags=['product'])
api_router.include_router(
    webhooks.router, prefix='/webhooks', tags=['webhook'])
api_router.include_router(
    company.router, prefix='/companies', tags=['product', 'compnay'])
api_router.include_router(
    series.router, prefix='/series', tags=['product', 'series'])
api_router.include_router(
    category.router, prefix='/categories', tags=['product', 'category'])
api_router.include_router(
    sculptor.router, prefix='/sculptors', tags=['product', 'sculptor', 'worker'])
api_router.include_router(
    paintwork.router, prefix='/paintworks', tags=['product', 'paintwork', 'worker'])
api_router.include_router(
    source_checksum.router, prefix='/source-checksums', tags=['source-checksum'])
api_router.include_router(
    application.router, prefix='/applications', tags=['application'])
