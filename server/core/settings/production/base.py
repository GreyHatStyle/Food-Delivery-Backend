import os

DEBUG = True

ALLOWED_HOSTS = [
    os.environ.get("ALLOWED_HOST_URL_PROD")
]

CORS_ALLOWED_ORIGINS = [
    "https://food-delivery-frontend-lake.vercel.app",
    os.environ.get("ALLOWED_HOST_URL_FOR_FUTURE"),  
]