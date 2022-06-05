import pytest
from app.models import Series
from sqlalchemy.orm import Session


@pytest.mark.usefixtures("db")
class TestSeries:
    def test_as_unique(self, db: Session):
        series = Series.as_unique(db, name="Fate")
        same_series = Series.as_unique(db, name="Fate")
        another_series = Series.as_unique(db, name="GBF")

        assert series is same_series
        assert another_series is not series
        assert another_series is not same_series
