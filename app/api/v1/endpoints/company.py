from app import crud
from app.api import deps
from app.models import Company
from app.schemas.company import CompanyCreate, CompanyInDB, CompanyUpdate
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse, Response
from sqlalchemy.orm import Session
from app.schemas.page import Page, PageParamsBase

router = APIRouter()


def check_company_exist(company_id: str, db: Session = Depends(deps.get_db)) -> Company:
    company = crud.company.get(db=db, id=company_id)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Specified company(id:{company_id}) didn't exist."
        )
    return company


@router.get(
    '/',
    response_model=Page[CompanyInDB]
)
def get_companys(
    *,
    db: Session = Depends(deps.get_db),
    params: PageParamsBase = Depends()
):
    skip = (params.page - 1) * params.size
    companys = crud.company.get_multi(db=db, skip=skip, limit=params.size)
    companys_count = crud.company.count(db=db)
    companys_out = [
        CompanyInDB.from_orm(company)
        for company in companys
    ]
    return Page.create(
        results=companys_out,
        total_results=companys_count,
        params=params
    )


@router.post(
    '/',
    response_model=CompanyInDB,
    status_code=status.HTTP_201_CREATED,
)
def create_company(
    *,
    request: Request,
    db: Session = Depends(deps.get_db),
    company_in: CompanyCreate,
):
    company = db.query(
        Company
    ).filter(
        Company.name == company_in.name
    ).first()

    if company:
        return RedirectResponse(
            url=request.url_for('get_company', company_id=company.id),
            status_code=status.HTTP_303_SEE_OTHER
        )

    company = crud.company.create(db=db, obj_in=company_in)
    return CompanyInDB.from_orm(company)


@router.get('/{company_id}', response_model=CompanyInDB)
def get_company(
    *,
    company: Company = Depends(check_company_exist)
):
    return CompanyInDB.from_orm(company)


@router.put('/{company_id}', response_model=CompanyInDB)
def udpate_company(
    *,
    db: Session = Depends(deps.get_db),
    company: Company = Depends(check_company_exist),
    company_in: CompanyUpdate
):
    company = crud.company.update(db=db, db_obj=company, obj_in=company_in)
    return CompanyInDB.from_orm(company)


@router.delete('/{company_id}')
def delete_company(
    *,
    db: Session = Depends(deps.get_db),
    company: Company = Depends(check_company_exist),
):
    crud.company.remove(db=db, id=company.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
