
import pytest
from app.models import Task
from sqlalchemy.orm import Session


@pytest.mark.usefixtures("db")
class TestCompany:
    def test_as_unique(self, db: Session):
        task = Task.as_unique(db, name="foo")
        same_task = Task.as_unique(db, name="foo")
        another_task = Task.as_unique(db, name="bar")

        assert task is same_task
        assert another_task is not task
        assert another_task is not same_task
