from logging import INFO, LogRecord

import pytest
from app.utils.logging.log_filters import (AccessApplicationFilter,
                                           application_name, application_uuid)
from faker import Faker


@pytest.fixture
def uuid(faker: Faker):
    """Set and return uuid of application"""
    uuid = faker.uuid4()
    application_uuid.set(uuid)
    return uuid


@pytest.fixture
def app_name(faker: Faker):
    """Set and return name of application"""
    name = faker.name()
    application_name.set(name)
    return name


@pytest.fixture
def log_record():
    """Create a log record at INFO-level."""
    record = LogRecord(
        name="",
        level=INFO,
        pathname="",
        lineno=0,
        msg="Kappa",
        args=(),
        exc_info=None
    )
    return record


def test_filter_adds_application_info(app_name, uuid, log_record):
    filter_ = AccessApplicationFilter()
    filter_.filter(log_record)
    assert log_record.application_name == app_name
    assert log_record.application_uuid == uuid
