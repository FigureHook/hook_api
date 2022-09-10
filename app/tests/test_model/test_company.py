import pytest
from app.models import Company
from sqlalchemy.orm import Session


@pytest.mark.usefixtures("db")
class TestCompany:
    def test_as_unique(self, db: Session):
        company = Company.as_unique(db, name="foo")
        same_company = Company.as_unique(db, name="foo")
        another_company = Company.as_unique(db, name="bar")

        assert company is same_company
        assert another_company is not company
        assert another_company is not same_company
