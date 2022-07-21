from app import crud
from app.api import deps
from app.models import Paintwork
from app.schemas.page import Page, PageParamsBase
from app.schemas.worker import WorkerCreate, WorkerInDB, WorkerUpdate
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse, Response
from sqlalchemy.orm import Session

router = APIRouter()


def check_paintwork_exist(paintwork_id: int, db: Session = Depends(deps.get_db)) -> Paintwork:
    paintwork = crud.paintwork.get(db=db, id=paintwork_id)
    if not paintwork:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Specified paintwork(id:{paintwork_id}) didn't exist."
        )
    return paintwork


@router.get('/', response_model=Page[WorkerInDB])
def get_paintworks(
    *,
    db: Session = Depends(deps.get_db),
    params: PageParamsBase = Depends()
):
    skip = (params.page - 1) * params.size
    workers = crud.paintwork.get_multi(db=db, skip=skip, limit=params.size)
    workers_count = crud.paintwork.count(db=db)
    workers_out = [
        WorkerInDB.from_orm(worker)
        for worker in workers
    ]
    return Page.create(
        results=workers_out,
        total_results=workers_count,
        params=params
    )


@router.post('/', response_model=WorkerInDB, status_code=status.HTTP_201_CREATED)
def create_paintwork(
    *,
    request: Request,
    db: Session = Depends(deps.get_db),
    worker_in: WorkerCreate
):
    paintwork = db.query(
        Paintwork
    ).filter(
        Paintwork.name == worker_in.name
    ).first()

    if paintwork:
        return RedirectResponse(
            url=request.url_for('get_paintwork', paintwork_id=paintwork.id),
            status_code=status.HTTP_303_SEE_OTHER
        )

    paintwork = crud.paintwork.create(db=db, obj_in=worker_in)
    return WorkerInDB.from_orm(paintwork)


@router.get('/{paintwork_id}', response_model=WorkerInDB)
def get_paintwork(
    *,
    paintwork: Paintwork = Depends(check_paintwork_exist)
):
    return WorkerInDB.from_orm(paintwork)


@router.put('/{paintwork_id}', response_model=WorkerInDB)
def update_paintwork(
    *,
    db: Session = Depends(deps.get_db),
    paintwork: Paintwork = Depends(check_paintwork_exist),
    worker_in: WorkerUpdate
):
    paintwork = crud.paintwork.update(
        db=db, db_obj=paintwork, obj_in=worker_in)
    return WorkerInDB.from_orm(paintwork)


@router.delete('/{paintwork_id}')
def delete_paintwork(
    *,
    db: Session = Depends(deps.get_db),
    paintwork: Paintwork = Depends(check_paintwork_exist),
):
    crud.paintwork.remove(db=db, id=paintwork.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
