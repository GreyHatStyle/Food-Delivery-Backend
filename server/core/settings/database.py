import os

import mongoengine
import logging

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_TABLE"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": os.environ.get("DB_PORT"),
    }
}

# Disable mongoengine logging
logging.getLogger('mongoengine').setLevel(logging.WARNING)
logging.getLogger('pymongo').setLevel(logging.WARNING)


mongoengine.connect(
    db=os.environ.get("MONGO_DB_NAME"),
    host=os.environ.get("MONGO_DB_HOST"),
    connect=os.environ.get("MONGO_CONNECT", "") == "True",
    # Just preventing it to connect on start server
    # (so that I can perform management commands without getting this function's messages)
)
