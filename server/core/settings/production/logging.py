"""
IN PRODUCTION MODE THIS LOGGING IS GIVING SOME ISSUES KINDLY DEAL WITH THIS
"""

import os

from django.conf import settings
from dotenv import load_dotenv
from utils import LogSetup

load_dotenv()

logger_util = LogSetup(settings.APPS_TO_LOG)

# Better stack (logtail)
source_token = os.environ.get("BETTERSTACK_SOURCE_TOKEN", "")
host = f'https://{os.environ.get("BETTERSTACK_INGESTING_HOST", "")}'

print(source_token)
print("HOST: ", host)

app_handlers = {}
app_loggers = {}

if len(app_handlers) == 0 and len(app_loggers) == 0:
    for app in settings.APPS_TO_LOG:
        app_handlers.update(
            logger_util.create_logtail_app_handlers(app, source_token, host)
        )
        app_loggers.update(logger_util.create_app_logger(app))

# Logs
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        # Main BetterStack handler (fallback)
        "logtail": {
            "class": "logtail.LogtailHandler",
            "source_token": source_token,
            "host": host,
            "level": "INFO",
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
            "level": os.environ.get("DJANGO_LOG_LEVEL", "INFO"),
            "handlers": ["logtail"],
        },
        # Django internal loggers
        "django": {
            "level": "INFO",
            "handlers": ["logtail"],
            "propagate": False,
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
