import pytest
from app.models import Paintwork, Sculptor
from sqlalchemy.orm import Session


@pytest.mark.usefixtures("db")
class TestSculptor:
    def test_as_unique(self, db: Session):
        sculptor = Sculptor.as_unique(db, name="foo")
        same_sculptor = Sculptor.as_unique(db, name="foo")
        another_sculptor = Sculptor.as_unique(db, name="bar")

        assert sculptor is same_sculptor
        assert another_sculptor is not sculptor
        assert another_sculptor is not same_sculptor

    def test_multiple_sculptors_as_unique(self, db: Session):
        master = Sculptor(name="master")
        db.add(master)
        db.commit()

        sculptors_in_text = ["master", "newbie"]
        sculptors = Sculptor.multiple_as_unique(db, sculptors_in_text)

        assert isinstance(sculptors, list)
        assert len(sculptors) == len(sculptors_in_text)
        assert master in sculptors


@pytest.mark.usefixtures("db")
class TestPaintwork:
    def test_as_unique(self, db: Session):
        paintwork = Paintwork.as_unique(db, name="foo")
        same_paintwork = Paintwork.as_unique(db, name="foo")
        another_paintwork = Paintwork.as_unique(db, name="bar")

        assert paintwork is same_paintwork
        assert another_paintwork is not paintwork
        assert another_paintwork is not same_paintwork

    def test_multiple_sculptors_as_unique(self, db: Session):
        master = Paintwork(name="master")
        db.add(master)
        db.commit()

        sculptors_in_text = ["master", "newbie"]
        sculptors = Paintwork.multiple_as_unique(db, sculptors_in_text)

        assert isinstance(sculptors, list)
        assert len(sculptors) == len(sculptors_in_text)
        assert master in sculptors
