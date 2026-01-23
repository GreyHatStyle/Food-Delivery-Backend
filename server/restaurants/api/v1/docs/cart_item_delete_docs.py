from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
    inline_serializer,
)
from rest_framework import serializers


delete_cart_item_schema = extend_schema(
    summary="Delete Cart Item",
    description="Removes item from cart (no matter how much quantity it has) at single request.",
    responses={
        200: OpenApiResponse(
            response=inline_serializer(
                name="AddItemResponse",
                fields={
                    "category": serializers.ChoiceField(["success", "error"]),
                    "result": serializers.CharField(),
                },
            ),
            description='Item is removed from cart at once (even if quantity was 10).',
            examples=[
                OpenApiExample(
                    "Success",
                    value={
                        "status": "success",
                        "result": "Cart Item 221 has been deleted!!"
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
        403: OpenApiResponse(
            response=inline_serializer(
                name="AccessingSomeoneElseError",
                fields={
                    "status": serializers.CharField(),
                    "message": serializers.CharField(),
                },
            ),
            description="If user 'test2' tries to access someone else cart item, (even if he knows their cart item id), server will forbid it securing another user's order details from 'test2' user",
            examples=[
                OpenApiExample(
                    "Authentication Failed",
                    value={
                    "status": "error",
                    "message": "Cart Item for user test2, with this Id 1 doesn't exist"
                },
                )
            ],
        ),
    },
    tags=["restaurants"],
    operation_id="delete_cart_item",
)
