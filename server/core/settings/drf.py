

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "EXCEPTION_HANDLER": "utils.token_exception_handler.handler_function",
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
        "utils.global_throttles.BurstRateThrottle",
        "utils.global_throttles.AnonBurstRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "500/day",
        "user": "1500/day",
        "login_scope": "14/day",
        "burst": "30/minute",
        "anon_burst": "20/minute"
    },
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
}
