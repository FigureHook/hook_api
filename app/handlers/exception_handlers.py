import logging

from fastapi import Request
from fastapi.responses import PlainTextResponse
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    logger.exception(exc)
    return PlainTextResponse("Internal server error.", status_code=500)
