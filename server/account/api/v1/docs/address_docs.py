from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
    inline_serializer,
)
from rest_framework import serializers

address_schema = extend_schema(
    summary="User Address",
    description="To retrieve all the User's Address information like pincode, city, etc.. using their token",
    request=inline_serializer(name="UserAddress", fields={}),
    responses={
        200: OpenApiResponse(
            response=inline_serializer(
                name="SuccessResponse",
                fields={
                    "status": serializers.CharField(),
                    "message": serializers.CharField(),
                    "results": serializers.ListField()
                },
            ),
            description="Returns all the addresses saved by User",
            examples=[
                OpenApiExample(
                    "Success",
                    value={
                        "status": "success", 
                        "message": "User test1's all address found successfully",
                        "results": [
                            {
                                "id": 1,
                                "main_address": "A-999, ABC colony",
                                "city": "city1",
                                "state": "state1",
                                "pin_code": "XXXXXX",
                                "address_type": "HOM",
                                "updated_at": "2025-11-18T17:14:30.123456+05:30"
                            },
                            {
                                "id": 2,
                                "main_address": "A-888 XYZ hostel",
                                "city": "city2",
                                "state": "state2",
                                "pin_code": "XXXXXX",
                                "address_type": "OTH",
                                "updated_at": "2025-11-18T17:04:35.123456+05:30"
                            }
                        ]
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
    operation_id="address_docs",
)
