from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
    inline_serializer,
)
from rest_framework import serializers

health_schema = extend_schema(
    summary="Health Check",
    description="To check whether the server is working or not",
    request=inline_serializer(name="HealthCheck", fields={}),
    auth=[],
    responses={
        200: OpenApiResponse(
            response=inline_serializer(
                name="SuccessResponse",
                fields={
                    "status": serializers.CharField(),
                    "message": serializers.CharField(),
                },
            ),
            description="API is working fine",
            examples=[
                OpenApiExample(
                    "Success",
                    value={"status": "success", "message": "Api working fine"},
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
