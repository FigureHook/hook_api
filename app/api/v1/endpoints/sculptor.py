from app import crud
from app.api import deps
from app.models import Sculptor
from app.schemas.worker import WorkerCreate, WorkerInDB, WorkerUpdate
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

router = APIRouter()


def check_sculptor_exist(sculptor_id: int, db: Session = Depends(deps.get_db)) -> Sculptor:
    sculptor = crud.sculptor.get(db=db, id=sculptor_id)
    if not sculptor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Specified sculptor(id:{sculptor_id}) didn't exist."
        )
    return sculptor


@router.get('/', response_model=list[WorkerInDB])
def get_sculptors(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
):
    workers = crud.sculptor.get_multi(db=db, skip=skip, limit=limit)
    return [
        WorkerInDB.from_orm(worker)
        for worker in workers
    ]


@router.post('/', response_model=WorkerInDB, status_code=status.HTTP_201_CREATED)
def create_sculptor(
    *,
    request: Request,
    db: Session = Depends(deps.get_db),
    worker_in: WorkerCreate
):
    sculptor = db.query(
        Sculptor
    ).filter(
        Sculptor.name == worker_in.name
    ).first()

    if sculptor:
        return RedirectResponse(
            url=request.url_for('get_sculptor', sculptor_id=sculptor.id),
            status_code=status.HTTP_303_SEE_OTHER
        )

    sculptor = crud.sculptor.create(db=db, obj_in=worker_in)
    return WorkerInDB.from_orm(sculptor)


@router.get('/{sculptor_id}', response_model=WorkerInDB)
def get_sculptor(
    *,
    sculptor: Sculptor = Depends(check_sculptor_exist)
):
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
    return WorkerInDB.from_orm(sculptor)


@router.delete('/{sculptor_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_sculptor(
    *,
    db: Session = Depends(deps.get_db),
    sculptor: Sculptor = Depends(check_sculptor_exist),
):
    crud.sculptor.remove(db=db, id=sculptor.id)
