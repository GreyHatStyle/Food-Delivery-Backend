from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
    inline_serializer,
)
from rest_framework import serializers

from ..serializers import LoginValidation

login_schema_for_docs = extend_schema(
    summary="User Login",
    description="Authenticate user and return JWT tokens for access and refresh, with user's details to be stored in frontend storage",
    request=LoginValidation,
    auth=[],
    examples=[
        OpenApiExample(
            "Login Example",
            summary="Example login credentials",
            description="Use these credentials to test the login endpoint",
            value={"username": "test_user", "password": "test_password"},
            request_only=True,  # This makes it only show for requests
        ),
    ],
    responses={
        200: OpenApiResponse(
            response=inline_serializer(
                name="LoginResponse",
                fields={
                    "status": serializers.CharField(),
                    "message": serializers.CharField(),
                    "user": inline_serializer(
                        name="UserInfo",
                        fields={
                            "id": serializers.CharField(),
                            "username": serializers.CharField(),
                            "email": serializers.EmailField(),
                            "first_name": serializers.CharField(),
                            "last_name": serializers.CharField(),
                            "phone_no": serializers.CharField(),
                        },
                    ),
                    "tokens": inline_serializer(
                        name="TokenPair",
                        fields={
                            "refresh": serializers.CharField(),
                            "access": serializers.CharField(),
                        },
                    ),
                },
            ),
            description="Login successful",
            examples=[
                OpenApiExample(
                    "Success",
                    value={
                        "status": "success",
                        "message": "Logged in successfully!!",
                        "user": {
                            "id": "123e4567-e89b-12d3-a456-426614174000",
                            "username": "test_user",
                            "email": "test_user@email.com",
                            "first_name": "Test",
                            "last_name": "User",
                            "phone_no": "+91999999999"
                        },
                        "tokens": {
                            "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                            "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                        },
                    },
                )
            ],
        ),
        400: OpenApiResponse(
            response=inline_serializer(
                name="ValidationError",
                fields={
                    "status": serializers.CharField(),
                    "message": serializers.CharField(),
                    "errors": inline_serializer(
                        name="Erros",
                        fields={
                            "username": serializers.ListField(
                                child=serializers.CharField(),
                            ),
                            "password": serializers.ListField(
                                child=serializers.CharField()
                            ),
                            "extra_fields": serializers.ListField(
                                child=serializers.CharField(required=False),
                            ),
                        },
                    ),
                },
            ),
            description="Validation Failed",
            examples=[
                OpenApiExample(
                    "Validation Errors",
                    value={
                        "status": "failed",
                        "message": "Username cannot be empty",
                        "errors": {
                            "username": ["Username cannot be empty"],
                            "password": ["Password cannot be empty"],
                            "extra_fields": ["Please remove extra fields: extra"],
                        },
                    },
                ),
            ],
        ),
        401: OpenApiResponse(
            response=inline_serializer(
                name="LoginError",
                fields={
                    "status": serializers.CharField(),
                    "message": serializers.CharField(),
                },
            ),
            description="Authentication failed",
            examples=[
                OpenApiExample(
                    "Authentication Failed",
                    value={
                        "status": "failed",
                        "message": "Username or Password is Incorrect, 3 attempts left",
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
    operation_id="user_login",
)
