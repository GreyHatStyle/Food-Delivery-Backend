import os
from pathlib import Path

from dotenv import load_dotenv

# This noqa will ignore warning of "flake8" related to this issue in this file only.
from split_settings.tools import include, optional  # noqa: F401

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
ENVIRONMENT_SETTINGS = os.environ.get("ENVIRONMENT_MODE", "production")

include(
    "base.py",
    f"{ENVIRONMENT_SETTINGS}/__init__.py",
    "database.py",
    "drf.py",
    "simple_jwt.py",
    "scalar.py",
)
