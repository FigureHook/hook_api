import pytest
from app.constants import SourceSite
from app.models import SourceChecksum
from sqlalchemy.orm import Session


@pytest.mark.usefixtures("db")
class TestSourceChecksum:
    def test_sourcechecksum_as_unique(self, db: Session):
        checksum = "kappa"
        s = SourceChecksum(
            source=SourceSite.GSC_ANNOUNCEMENT,
            checksum=checksum
        )
        db.add(s)
        db.commit()

        fetched_source = SourceChecksum.as_unique(
            db, source=SourceSite.GSC_ANNOUNCEMENT)
        assert fetched_source == s
