from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
    inline_serializer,
)
from rest_framework import serializers

user_verify_schema = extend_schema(
    summary="User Verify",
    description="To check whether the server is working or not",
    request=inline_serializer(name="HealthCheck", fields={}),
    responses={
        200: OpenApiResponse(
            response=inline_serializer(
                name="SuccessResponse",
                fields={
                    "status": serializers.CharField(),
                    "message": serializers.CharField(),
                },
            ),
            description="Correct Access token in header",
            examples=[
                OpenApiExample(
                    "Success",
                    value={"status": "success", "message": "test_user is given"},
                )
            ],
        ),
        401: OpenApiResponse(
            response=inline_serializer(
                name="UnAuthorized",
                fields={
                    "detail": serializers.CharField(),
                },
            ),
            description="Wrong or No access token in Header",
            examples=[
                OpenApiExample(
                    "Fail",
                    value={
                        "status": "failed",
                        "detail": "Given token not valid for any token type.",
                        "message": "Token is either expired or not valid.",
                    },
                )
            ],
        ),
        500: OpenApiResponse(
            response=inline_serializer(
                name="LoginError",
                fields={
                    "status": serializers.CharField(),
                    "reason": serializers.CharField(),
                    "message": serializers.CharField(),
                },
            ),
            description="Server Error",
            examples=[
                OpenApiExample(
                    "Server Error",
                    value={
                        "status": "exception",
                        "reason": "Some reason because of which server could not give response",
                        "message": "message to show user",
                    },
                )
            ],
        ),
    },
    tags=["account"],
    operation_id="health_check",
)
