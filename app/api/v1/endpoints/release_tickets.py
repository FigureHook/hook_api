import logging
import uuid

from app.api import deps
from app.helpers.orm_helper import ReleaseFeedOrmHelper
from app.models import ReleaseTicket
from app.models.product import ProductReleaseInfo
from app.schemas.page import Page, PageParamsBase
from app.schemas.release_feed import (ReleaseFeed, ReleaseTicketCreate,
                                      ReleaseTicketInDB)
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

router = APIRouter()
logger = logging.getLogger(__name__)


def valid_uuid_hex(ticket_id: str) -> bool:
    try:
        uuid.UUID(hex=ticket_id)
    except ValueError:
        return False
    return True


def check_ticket_exist(
    ticket_id: str,
    db: Session = Depends(deps.get_db)
) -> ReleaseTicket:
    if valid_uuid_hex(ticket_id=ticket_id):
        ticket_uid = uuid.UUID(hex=ticket_id)
        ticket = db.get(ReleaseTicket, ident=ticket_uid)
        if ticket:
            return ticket

    logger.info(
        f"Specified release-ticket didn't exist. (id={ticket_id})")
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Specified release-ticket(id: {ticket_id}) didn't exist."
    )


@router.get(
    '/',
    response_model=Page[ReleaseTicketInDB]
)
async def get_multi_release_tickets(
    *,
    db: Session = Depends(deps.get_db),
    page_params: PageParamsBase = Depends()
):
    stmt = select(ReleaseTicket).offset(
        page_params.skip).limit(page_params.size)
    tickets = db.scalars(stmt).unique().all()

    count_stmt = select(func.count(ReleaseTicket.id))
    tickets_count = db.scalar(count_stmt)

    tickets_out = [
        ReleaseTicketInDB(id=ticket.id.hex, created_at=ticket.created_at)
        for ticket in tickets
    ]

    return Page.create(
        results=tickets_out,
        total_results=tickets_count,
        params=page_params
    )


@router.post(
    '/',
    response_model=ReleaseTicketInDB,
    status_code=status.HTTP_201_CREATED
)
async def create_ticket(
    *,
    db: Session = Depends(deps.get_db),
    ticket_info: ReleaseTicketCreate
):
    stmt = select(ProductReleaseInfo).filter(
        ProductReleaseInfo.announced_at != None,
        ProductReleaseInfo.announced_at > ticket_info.from_,
        ProductReleaseInfo.created_at >= ticket_info.from_,
    )
    future_releases = db.scalars(stmt).unique().all()
    ticket = ReleaseTicket()
    ticket.release_infos = future_releases
    db.add(ticket)
    db.commit()

    logger.info(
        f"Created the release-ticket. (id={ticket.id}, from={ticket_info.from_.isoformat()})")
    return ReleaseTicketInDB(id=ticket.id.hex, created_at=ticket.created_at)


@router.get(
    '/{ticket_id}',
    response_model=list[ReleaseFeed]
)
async def get_ticket(
    *,
    ticket: ReleaseTicket = Depends(check_ticket_exist),
    db: Session = Depends(deps.get_db)
):
    release_ids = [
        info.id
        for info in ticket.release_infos
    ]
    release_feeds = ReleaseFeedOrmHelper.fetch_release_feed_by_ids(
        db, release_ids=release_ids
    )

    logger.info(f"Fetched release-ticket. (id={ticket.id}, type='feed')")
    return release_feeds


@router.delete(
    '/{ticket_id}',
    status_code=204
)
async def delete_ticket(
    *,
    ticket: ReleaseTicket = Depends(check_ticket_exist),
    db: Session = Depends(deps.get_db)
):
    db.delete(ticket)
    db.commit()

    logger.info(f"Removed the release-ticket. (id={ticket.id})")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
