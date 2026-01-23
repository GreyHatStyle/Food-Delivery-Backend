from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
    inline_serializer,
)
from rest_framework import serializers

cart_delete_schema = extend_schema(
    summary="Empty Cart Details",
    description="Basically Clear Cart, removes all cart information with its cart items details at once from backend.",
    request=inline_serializer(name="CartRemove", fields={}),
    responses={
        200: OpenApiResponse(
            response=inline_serializer(
                name="SuccessResponse",
                fields={
                    "status": serializers.ChoiceField(["success", "error", "exception",]),
                    "message": serializers.CharField(), 
                },
            ),
            description="Cart is emptied successfully",
            examples=[
                OpenApiExample(
                    "Success",
                    value={
                        "status": "success",
                        "message": "Cart with 15 of user test2 has been deleted"
                    },
                )
            ],
        ),
        401: OpenApiResponse(
            response=inline_serializer(
                name="LoginError",
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
                name="ServerError",
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
    tags=["restaurants"],
    operation_id="cart_manage_delete",
)

