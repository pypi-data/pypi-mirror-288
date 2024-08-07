"""
...
"""

import os

from pathlib import Path


# Project

ENVIRONMENT = os.environ.get("ENVIRONMENT", None)
DEBUG = os.environ.get("DEBUG", None)
LOGGING_LEVEL = os.environ.get("DEBUG", None)

# Database

DB_NAME = os.environ.get("DB_NAME", None)
DB_USER = os.environ.get("DB_USER", None)
DB_PASSWORD = os.environ.get("DB_PASSWORD", None)
DB_HOST = os.environ.get("DB_HOST", None)
DB_PORT = os.environ.get("DB_PORT", None)
DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

BASE_DIR = Path(__file__).resolve().parent.parent
ROUTERS_FOLDER = "routers"
MODELS_FOLDER = "models"

API_PREFIX = "/"
TRAILING_SLASH = True