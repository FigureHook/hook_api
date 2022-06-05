import pytest
from app.models import Category
from sqlalchemy.orm import Session


@pytest.mark.usefixtures("db")
class TestCompany:
    def test_as_unique(self, db: Session):
        category = Category.as_unique(db, name="foo")
        same_category = Category.as_unique(db, name="foo")
        another_category = Category.as_unique(db, name="bar")

        assert category is same_category
        assert another_category is not category
        assert another_category is not same_category
