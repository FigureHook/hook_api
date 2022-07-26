from logging import Filter
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from logging import LogRecord


class AccessApplicationFilter(Filter):
    """Logging filter to attached application name and UUIDs to log records"""
    application_uuid: Optional[str] = None
    application_name: Optional[str] = None

    @classmethod
    def set_app_uuid(cls, uuid: str):
        cls.application_uuid = uuid

    @classmethod
    def set_app_name(cls, name: str):
        cls.application_name = name

    def filter(self, record: 'LogRecord') -> bool:
        """
        Attach the accessing application name and UUID to the log record.
        """
        record.application_uuid = self.application_uuid  # type: ignore
        record.application_name = self.application_name  # type: ignore
        return True
