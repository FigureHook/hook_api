import logging

from app import crud
from app.api import deps
from app.models import Series
from app.schemas.page import Page, PageParamsBase
from app.schemas.series import SeriesCreate, SeriesInDB, SeriesUpdate
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse, Response
from sqlalchemy import select
from sqlalchemy.orm import Session

router = APIRouter()
logger = logging.getLogger(__name__)


def check_series_exist(series_id: str, db: Session = Depends(deps.get_db)) -> Series:
    series = crud.series.get(db=db, id=series_id)
    if not series:
        logger.info(
            f"Specified series didn't exist. (id={series_id})"
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Specified series(id:{series_id}) didn't exist."
        )
    return series


@router.get(
    '/',
    response_model=Page[SeriesInDB]
)
def get_series_multi(
    *,
    db: Session = Depends(deps.get_db),
    page_params:  PageParamsBase = Depends()
):
    series_list = crud.series.get_multi(db=db, skip=page_params.skip, limit=page_params.size)
    series_count = crud.series.count(db=db)
    series_out = [
        SeriesInDB.from_orm(series)
        for series in series_list
    ]
    logger.info(f"Fetched the series. (count={len(series_out)})")
    return Page.create(
        results=series_out,
        total_results=series_count,
        params=page_params
    )


@router.post(
    '/',
    response_model=SeriesInDB,
    status_code=status.HTTP_201_CREATED,
)
def create_series(
    *,
    request: Request,
    db: Session = Depends(deps.get_db),
    series_in: SeriesCreate,
):
    stmt = select(Series).filter_by(name=series_in.name).limit(1)
    series = db.scalars(stmt).first()
    if series:
        logger.info(
            f"The series already exists. (id={series.id}, name={series.name})")
        return RedirectResponse(
            url=request.url_for('get_series', series_id=series.id),
            status_code=status.HTTP_303_SEE_OTHER
        )

    series = crud.series.create(db=db, obj_in=series_in)
    logger.info(f"Created the series. (id={series.id})")
    return SeriesInDB.from_orm(series)


@router.get('/{series_id}', response_model=SeriesInDB)
def get_series(
    *,
    series: Series = Depends(check_series_exist)
):
    logger.info(f"Fetched the series. (id={series.id})")
    return SeriesInDB.from_orm(series)


@router.put('/{series_id}', response_model=SeriesInDB)
def udpate_series(
    *,
    db: Session = Depends(deps.get_db),
    series: Series = Depends(check_series_exist),
    series_in: SeriesUpdate
):
    series = crud.series.update(db=db, db_obj=series, obj_in=series_in)
    logger.info(f"Updated the series. (id={series.id})")
    return SeriesInDB.from_orm(series)


@router.delete('/{series_id}')
def delete_series(
    *,
    db: Session = Depends(deps.get_db),
    series: Series = Depends(check_series_exist),
):
    crud.series.remove(db=db, id=series.id)
    logger.info(f"Removed the series. (id={series.id})")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
