from datetime import datetime

import pytest
from app.constants import SourceSite
from app.models import SourceChecksum
from sqlalchemy.orm import Session


@pytest.mark.usefixtures("db")
class TestSourceChecksum:
    def test_fetch_checksum_by_source(self, db: Session):
        checksum = "kappa"
        s = SourceChecksum(
            source=SourceSite.GSC_ANNOUNCEMENT,
            checksum=checksum
        )
        db.add(s)
        db.commit()

        site_checksum = SourceChecksum.get_by_site(
            db, SourceSite.GSC_ANNOUNCEMENT)
        assert site_checksum
        assert site_checksum.checksum == checksum
        assert isinstance(site_checksum.checked_at, datetime)

    def test_sourcechecksum_as_unique(self, db: Session):
        checksum = "kappa"
        s = SourceChecksum(
            source=SourceSite.GSC_ANNOUNCEMENT,
            checksum=checksum
        )
        db.add(s)
        db.commit()

        fetched_source = SourceChecksum.as_unique(
            db, SourceSite.GSC_ANNOUNCEMENT)
        assert fetched_source == s
