import logging

from app import crud
from app.api import deps
from app.models import Sculptor
from app.schemas.page import Page, PageParamsBase
from app.schemas.worker import WorkerCreate, WorkerInDB, WorkerUpdate
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse, Response
from sqlalchemy.orm import Session
from sqlalchemy import select

router = APIRouter()
logger = logging.getLogger(__name__)


def check_sculptor_exist(sculptor_id: int, db: Session = Depends(deps.get_db)) -> Sculptor:
    sculptor = crud.sculptor.get(db=db, id=sculptor_id)
    if not sculptor:
        logger.info(f"Specified sculptor didn't exist. (id={sculptor_id})")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Specified sculptor(id:{sculptor_id}) didn't exist."
        )
    return sculptor


@router.get('/', response_model=Page[WorkerInDB])
def get_sculptors(
    *,
    db: Session = Depends(deps.get_db),
    params: PageParamsBase = Depends()
):
    skip = (params.page - 1) * params.size
    workers = crud.sculptor.get_multi(db=db, skip=skip, limit=params.size)
    workers_count = crud.sculptor.count(db=db)
    workers_out = [
        WorkerInDB.from_orm(worker)
        for worker in workers
    ]
    logger.info(f"Fetched the sculptors. (count={len(workers_out)})")
    return Page.create(
        results=workers_out,
        total_results=workers_count,
        params=params
    )


@router.post('/', response_model=WorkerInDB, status_code=status.HTTP_201_CREATED)
def create_sculptor(
    *,
    request: Request,
    db: Session = Depends(deps.get_db),
    worker_in: WorkerCreate
):
    stmt = select(Sculptor).filter_by(name=worker_in.name).limit(1)
    sculptor = db.scalars(stmt).first()
    if sculptor:
        logger.info(
            f"The sculptor already exists. (id={sculptor.id}, name={sculptor.name})")
        return RedirectResponse(
            url=request.url_for('get_sculptor', sculptor_id=sculptor.id),
            status_code=status.HTTP_303_SEE_OTHER
        )

    sculptor = crud.sculptor.create(db=db, obj_in=worker_in)
    logger.info(f"Created the sculptor. (id={sculptor.id})")
    return WorkerInDB.from_orm(sculptor)


@router.get('/{sculptor_id}', response_model=WorkerInDB)
def get_sculptor(
    *,
    sculptor: Sculptor = Depends(check_sculptor_exist)
):
    logger.info(f"Fetched the sculptor. (id={sculptor.id})")
    return WorkerInDB.from_orm(sculptor)


@router.put('/{sculptor_id}', response_model=WorkerInDB)
def update_sculptor(
    *,
    db: Session = Depends(deps.get_db),
    sculptor: Sculptor = Depends(check_sculptor_exist),
    worker_in: WorkerUpdate
):
    sculptor = crud.sculptor.update(
        db=db, db_obj=sculptor, obj_in=worker_in)
    logger.info(f"Updated the sculptor. (id={sculptor.id})")
    return WorkerInDB.from_orm(sculptor)


@router.delete('/{sculptor_id}')
def delete_sculptor(
    *,
    db: Session = Depends(deps.get_db),
    sculptor: Sculptor = Depends(check_sculptor_exist),
):
    crud.sculptor.remove(db=db, id=sculptor.id)
    logger.info(f"Removed the sculptor. (id={sculptor.id})")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
