from .base import STATIC_URL

SCALAR_THEME = "dark"

SCALAR_SETTINGS = {"defaultHttpClient": {"targetKey": "shell", "clientKey": "curl"}}


SPECTACULAR_SETTINGS = {
    "TITLE": "Restaurant WebApp Backend Server API",
    "DESCRIPTION": "This API documentation is to show functionality of all the backend APIs used by frontend",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    # available SwaggerUI configuration parameters
    # https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "persistAuthorization": True,
        "displayOperationId": True,
    },
    # available SwaggerUI versions: https://github.com/swagger-api/swagger-ui/releases
    "SWAGGER_UI_DIST": "https://cdn.jsdelivr.net/npm/swagger-ui-dist@latest",  # default
    "SWAGGER_UI_FAVICON_HREF": STATIC_URL
    + "your_company_favicon.png",  # default is swagger favicon
}
