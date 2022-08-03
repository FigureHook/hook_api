import uuid

import pytest
from app.models import Application
from sqlalchemy.orm import Session


@pytest.mark.usefixtures("db")
class TestApplication:
    def test_create_application(self, db: Session):
        application = Application(name="backend")
        db.add(application)
        db.commit()

        assert type(application.id) is uuid.UUID
        assert type(application.token) is str

    def test_regenerate_token(self, db: Session):
        application = Application(name="frontend")
        db.add(application)
        db.commit()

        prev_token = application.token
        application.refresh_token()
        new_token = application.token

        assert prev_token != new_token

    def test_application_was_seen(self, db:Session):
        application = Application(name="management")
        application.was_seen()
        db.add(application)
        db.commit()
        db.refresh(application)
        assert application.last_seen_at
