from core.settings.base import INSTALLED_APPS, MIDDLEWARE


DEBUG = True

ALLOWED_HOSTS = [
    "127.0.0.1",
    "[::1]",
    "localhost",
]

CORS_ALLOWED_ORIGINS = ["http://localhost:5173", "http://192.168.208.139:5173"]

INSTALLED_APPS += [
    'silk',
]
SILKY_PYTHON_PROFILER = True

MIDDLEWARE.insert(0, 'silk.middleware.SilkyMiddleware')