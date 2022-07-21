
from app import crud
from app.api import deps
from app.models import SourceChecksum
from app.schemas.source_checksum import (SourceChecksumCreate,
                                         SourceChecksumInDB,
                                         SourceChecksumUpdate)
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse, Response
from sqlalchemy.orm import Session

router = APIRouter()


def check_source_checksum_exist(
        source_checksum_id: int,
        db: Session = Depends(deps.get_db)
) -> SourceChecksum:
    source_checksum = crud.source_checksum.get(db=db, id=source_checksum_id)
    if not source_checksum:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Specified source-checksum(id: {source_checksum_id}) didn't exist."
        )
    return source_checksum


@router.get('/', response_model=list[SourceChecksumInDB])
def get_source_checksums(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
):
    source_checksums = crud.source_checksum.get_multi(
        db=db, skip=skip, limit=limit)
    return [
        SourceChecksumInDB.from_orm(source_checksum)
        for source_checksum in source_checksums
    ]


@router.post('/', response_model=SourceChecksumInDB, status_code=status.HTTP_201_CREATED)
def create_source_checksum(
    *,
    request: Request,
    db: Session = Depends(deps.get_db),
    source_checksum_in: SourceChecksumCreate
):
    source_checksum = db.query(SourceChecksum).filter(
        SourceChecksum.source == source_checksum_in.source
    ).first()
    if source_checksum:
        return RedirectResponse(
            request.url_for(
                'get_source_checksum',
                source_checksum_id=source_checksum.id),
            status_code=status.HTTP_303_SEE_OTHER
        )

    source_checksum = crud.source_checksum.create(
        db=db,
        obj_in=source_checksum_in)
    return SourceChecksumInDB.from_orm(source_checksum)


@router.get('/{source_checksum_id}', response_model=SourceChecksumInDB)
def get_source_checksum(
    *,
    source_checksum: SourceChecksum = Depends(check_source_checksum_exist)
):
    return SourceChecksumInDB.from_orm(source_checksum)


@router.patch('/{source_checksum_id}', response_model=SourceChecksumInDB)
def patch_source_checksum(
    *,
    db: Session = Depends(deps.get_db),
    source_checksum: SourceChecksum = Depends(check_source_checksum_exist),
    update_source_checksum: SourceChecksumUpdate
):
    source_checksum = crud.source_checksum.update(
        db=db, db_obj=source_checksum, obj_in=update_source_checksum)
    return SourceChecksumInDB.from_orm(source_checksum)


@router.delete(
    '/{source_checksum_id}')
def delete_source_checksum(
    *,
    db: Session = Depends(deps.get_db),
    source_checksum: SourceChecksum = Depends(check_source_checksum_exist)
):
    crud.source_checksum.remove(db=db, id=source_checksum.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
