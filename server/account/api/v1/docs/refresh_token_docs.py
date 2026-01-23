from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample, inline_serializer
from rest_framework import serializers

refresh_token_schema = extend_schema(
    summary="Refresh JWT Token",
    description="Get a new access and refresh token using previous refresh token, and then this 'last refresh' token gets blacklisted, so that it can not be used again",
    
    request=inline_serializer(
        name="TokenRefreshRequest",
        fields={
            "refresh": serializers.CharField(),
        },
    ),
    auth=[],
    examples=[
        OpenApiExample(
            "Refresh token example",
            summary="Example refresh",
            description="Use this body to test Refresh token API",
            value={"refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6Ikp..."},
            request_only=True,  # This makes it only show for requests
        ),
    ],
    responses={
        200: OpenApiResponse(
            response=inline_serializer(
                name="TokenRefreshResponse",
                fields={
                    "access": serializers.CharField(),
                    "refresh": serializers.CharField(),
                },
            ),
            description="If body's refresh token is valid and not blacklisted, it successfully returns new refresh and access token, and blacklist the body's refresh token ",
            examples=[
                OpenApiExample(
                    "Success",
                    value={
                        "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
                        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",    
                    },
                )
            ],
        ),
        401: OpenApiResponse(
            response=inline_serializer(
                name="AuthError",
                fields={
                    "status": serializers.CharField(),
                    "detail": serializers.CharField(),
                    "message": serializers.CharField(),
                },
            ),
            description="Authentication failed, when JWT token expires or sent wrong",
            examples=[
                OpenApiExample(
                    "Authentication Failed",
                    value={
                        "status": "failed",
                        "detail": "Given token not valid for any token type",
                        "message": "Token is either expired or not valid"
                    },
                )
            ],
        ),
    },
    tags=["account"],
    operation_id='refresh_token',
)