from contextvars import ContextVar
from logging import Filter
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from logging import LogRecord


application_uuid: ContextVar[Optional[str]] = ContextVar(
    "application_uuid", default=None
)

application_name: ContextVar[Optional[str]] = ContextVar(
    "application_name", default=None
)


class AccessApplicationFilter(Filter):
    """Logging filter to attached application name and UUIDs to log records"""

    def filter(self, record: "LogRecord") -> bool:
        """
        Attach the accessing application name and UUID to the log record.
        """
        record.application_uuid = application_uuid.get()  # type: ignore
        record.application_name = application_name.get()  # type: ignore
        return True
