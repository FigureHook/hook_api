from app.api import deps
from fastapi import APIRouter, Depends, Response

from .endpoints import (application, category, company, paintwork, products, release_tickets,
                        sculptor, series, source_checksum, webhooks)

api_router = APIRouter(dependencies=[Depends(deps.verify_token)])

api_router.include_router(
    products.router, prefix='/products', tags=['product'])
api_router.include_router(
    webhooks.router, prefix='/webhooks', tags=['discord', 'webhook', 'internal-service'])
api_router.include_router(
    company.router, prefix='/companies', tags=['product'])
api_router.include_router(
    series.router, prefix='/series', tags=['product'])
api_router.include_router(
    category.router, prefix='/categories', tags=['product'])
api_router.include_router(
    sculptor.router, prefix='/sculptors', tags=['product'])
api_router.include_router(
    paintwork.router, prefix='/paintworks', tags=['product'])
api_router.include_router(
    source_checksum.router, prefix='/source-checksums', tags=['source-checksum', 'internal-service'])
api_router.include_router(
    application.router, prefix='/applications', tags=['application', 'internal-service'])
api_router.include_router(
    release_tickets.router, prefix='/release-tickets', tags=['release-feed']
)
