from app import crud
from app.api import deps
from app.models import Series
from app.schemas.series import SeriesCreate, SeriesInDB, SeriesUpdate
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

router = APIRouter()


def check_series_exist(series_id: str, db: Session = Depends(deps.get_db)) -> Series:
    series = crud.series.get(db=db, id=series_id)
    if not series:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Specified series(id:{series_id}) didn't exist."
        )
    return series


@router.get(
    '/',
    response_model=list[SeriesInDB]
)
def get_series_multi(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
):
    series_list = crud.series.get_multi(db=db, skip=skip, limit=limit)
    return [
        SeriesInDB.from_orm(series)
        for series in series_list
    ]


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
    series = db.query(
        Series
    ).filter(
        Series.name == series_in.name
    ).first()

    if series:
        return RedirectResponse(
            url=request.url_for('get_series', series_id=series.id),
            status_code=status.HTTP_303_SEE_OTHER
        )

    series = crud.series.create(db=db, obj_in=series_in)
    return SeriesInDB.from_orm(series)


@router.get('/{series_id}', response_model=SeriesInDB)
def get_series(
    *,
    series: Series = Depends(check_series_exist)
):
    return SeriesInDB.from_orm(series)


@router.put('/{series_id}', response_model=SeriesInDB)
def udpate_series(
    *,
    db: Session = Depends(deps.get_db),
    series: Series = Depends(check_series_exist),
    series_in: SeriesUpdate
):
    series = crud.series.update(db=db, db_obj=series, obj_in=series_in)
    return SeriesInDB.from_orm(series)


@router.delete('/{series_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_series(
    *,
    db: Session = Depends(deps.get_db),
    series: Series = Depends(check_series_exist),
):
    crud.series.remove(db=db, id=series.id)
