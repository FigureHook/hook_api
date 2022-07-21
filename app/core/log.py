from logging.config import dictConfig

from .config import settings


def configure_logging() -> None:
    dictConfig(
        {
            'version': 1,
            'disable_existing_loggers': False,
            'filters': {  # correlation ID filter must be added here to make the %(correlation_id)s formatter work
                'correlation_id': {
                    '()': 'asgi_correlation_id.CorrelationIdFilter',
                    'uuid_length': 8 if not settings.ENVIRONMENT == 'development' else 32,
                },
            },
            'formatters': {
                "access_console": {
                    "()": "uvicorn.logging.AccessFormatter",
                    "fmt": '%(levelprefix)s %(client_addr)s - %(correlation_id)s - "%(request_line)s" %(status_code)s',  # noqa: E501
                },
                "access_file": {
                    "()": "uvicorn.logging.AccessFormatter",
                    "use_colors": False,
                    "fmt": '%(asctime)s - %(levelname)s - %(client_addr)s - %(correlation_id)s - "%(request_line)s" %(status_code)s',  # noqa: E501
                },
                'console': {
                    'class': 'logging.Formatter',
                    'format': '%(asctime)s - %(levelname)s - %(correlation_id)s <%(name)s:%(lineno)d> %(message)s',
                },
            },
            'handlers': {
                'uvicorn_access_console': {
                    'class': 'logging.StreamHandler',
                    'filters': ['correlation_id'],
                    'formatter': 'access_console',
                    'stream': "ext://sys.stdout"
                },
                'uvicorn_access_file': {
                    '()': 'logging.handlers.TimedRotatingFileHandler',
                    'filename': '/workspace/app/logs/uvicorn/access.log',
                    'when': 'D',
                    'encoding': 'utf-8',
                    'utc': True,
                    'filters': ['correlation_id'],
                    'formatter': 'access_file',
                },
                'app_default': {
                    '()': 'logging.handlers.TimedRotatingFileHandler',
                    'filename': '/workspace/app/logs/api/access.log',
                    'when': 'D',
                    'encoding': 'utf-8',
                    'utc': True,
                    'filters': ['correlation_id'],
                    'formatter': 'console'
                },
                'console': {
                    'class': 'logging.StreamHandler',
                    'filters': ['correlation_id'],
                    'formatter': 'console',
                    'stream': "ext://sys.stdout"
                }
            },
            # Loggers can be specified to set the log-level to log, and which handlers to use
            'loggers': {
                # project logger
                "app": {"handlers": ["app_default"], "level": "INFO"},
                "uvicorn.access": {"handlers": ["uvicorn_access_console", "uvicorn_access_file"], "level": "INFO", "propagate": False},
                'asgi_correlation_id': {'handlers': ['console'], 'level': 'WARNING'},
            },
        }
    )
