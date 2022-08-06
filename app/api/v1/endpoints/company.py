import logging

from app import crud
from app.api import deps
from app.models import Company
from app.schemas.company import CompanyCreate, CompanyInDB, CompanyUpdate
from app.schemas.page import Page, PageParamsBase
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse, Response
from sqlalchemy import select
from sqlalchemy.orm import Session

router = APIRouter()
logger = logging.getLogger(__name__)


def check_company_exist(company_id: str, db: Session = Depends(deps.get_db)) -> Company:
    company = crud.company.get(db=db, id=company_id)
    if not company:
        logger.info(f"Specified company didn't exist. (id={company_id})")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Specified company(id={company_id}) didn't exist."
        )
    return company


@router.get(
    '/',
    response_model=Page[CompanyInDB]
)
async def get_companies(
    *,
    db: Session = Depends(deps.get_db),
    page_params: PageParamsBase = Depends()
):
    companies = crud.company.get_multi(db=db, skip=page_params.skip, limit=page_params.size)
    companies_count = crud.company.count(db=db)
    companies_out = [
        CompanyInDB.from_orm(company)
        for company in companies
    ]
    logger.info(f"Fetched the companies. (count={len(companies_out)})")
    return Page.create(
        results=companies_out,
        total_results=companies_count,
        params=page_params
    )


@router.post(
    '/',
    response_model=CompanyInDB,
    status_code=status.HTTP_201_CREATED,
)
async def create_company(
    *,
    request: Request,
    db: Session = Depends(deps.get_db),
    company_in: CompanyCreate,
):
    stmt = select(Company).filter_by(name=company_in.name).limit(1)
    company = db.scalars(stmt).first()
    if company:
        logger.info(
            f"The company already exists. (id={company.id}, name={company.name})")
        return RedirectResponse(
            url=request.url_for('get_company', company_id=company.id),
            status_code=status.HTTP_303_SEE_OTHER
        )

    company = crud.company.create(db=db, obj_in=company_in)
    logger.info(f"Created the company. (id={company.id})")
    return CompanyInDB.from_orm(company)


@router.get('/{company_id}', response_model=CompanyInDB)
async def get_company(
    *,
    company: Company = Depends(check_company_exist)
):
    logger.info(f"Fetched the company. (id={company.id})")
    return CompanyInDB.from_orm(company)


@router.put('/{company_id}', response_model=CompanyInDB)
async def udpate_company(
    *,
    db: Session = Depends(deps.get_db),
    company: Company = Depends(check_company_exist),
    company_in: CompanyUpdate
):
    company = crud.company.update(db=db, db_obj=company, obj_in=company_in)
    logger.info(f"Updated the company. (id={company.id})")
    return CompanyInDB.from_orm(company)


@router.delete('/{company_id}')
async def delete_company(
    *,
    db: Session = Depends(deps.get_db),
    company: Company = Depends(check_company_exist),
):
    crud.company.remove(db=db, id=company.id)
    logger.info(f"Removed the company. (id={company.id})")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
