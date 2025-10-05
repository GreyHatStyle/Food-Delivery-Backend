import os

from django.conf import settings
from utils import LogSetup

logger_util = LogSetup(settings.APPS_TO_LOG)

app_handlers = {}
app_loggers = {}

for app in settings.APPS_TO_LOG:
    app_handlers.update(logger_util.create_file_app_handlers(app))
    app_loggers.update(logger_util.create_app_logger(app))


# Logs
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        # Console handler
        "console": {
            "class": "logging.StreamHandler",
            "level": os.environ.get("DJANGO_LOG_LEVEL", "DEBUG"),
            "formatter": "simple",
        },
        # General file handler (fallback)
        "general_file": {
            "class": "logging.FileHandler",
            "filename": str(logger_util.LOGS_DIR / "django.log"),
            "level": os.environ.get("DJANGO_LOG_LEVEL", "DEBUG"),
            "formatter": "verbose",
        },
        **app_handlers,
    },
    "filters": {
        "normal_level_filter": {
            "()": "django.utils.log.CallbackFilter",
            "callback": lambda record: record.levelno
            < 40,  # Less than ERROR level (40)
        },
    },
    "loggers": {
        # Root logger for other apps
        "": {
            "level": os.environ.get("DJANGO_LOG_LEVEL", "DEBUG"),
            "handlers": ["general_file", "console"],
        },
        **app_loggers,
    },
    "formatters": {
        "simple": {
            "format": "{levelname} [{asctime}]: {message}",
            "style": "{",
        },
        "verbose": {
            "format": "{levelname}[{asctime}] - ({name} -> {module}.py line={lineno:d}): {message}",
            "style": "{",
        },
    },
}
