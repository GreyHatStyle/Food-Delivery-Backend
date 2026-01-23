from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
    inline_serializer,
)
from rest_framework import serializers


add_remove_cart_item_schema = extend_schema(
    summary="Add Or Remove Cart Item",
    description="This post request can be used to add cart item in cart for first time and any number of times.",
    request=inline_serializer(
        name="CartItemBodySer",
        fields={
            "restaurant_id": serializers.UUIDField(),
            "item_uuid": serializers.UUIDField(),
            "category": serializers.CharField(max_length=50),
            "mode": serializers.ChoiceField([
                ("add", "Adds the provided menu item's uuid to cart (by 1)", ), 
                ("remove", "Removes the provided menu item's uuid from cart (by 1)", ), 
            ]),
        }
    ),
    examples=[
        OpenApiExample(
            "Add item example",
            summary="Example Add item example body",
            description="Use this body to add new item in cart",
            value={
                "restaurant_id": "6841313e-58bf-...",
                "item_uuid": "4ee5da0c-3ee7-...",
                "category": "Recommended",
                "mode": "add"
            },
            request_only=True,  # This makes it only show for requests
        ),
    ],
    responses={
        200: OpenApiResponse(
            response=inline_serializer(
                name="AddItemResponse",
                fields={
                    "id": serializers.IntegerField(),
                    "item_uuid": serializers.UUIDField(),
                    "category": serializers.CharField(max_length=50),
                    "quantity": serializers.IntegerField(),
                    "cart": serializers.IntegerField(),
                },
            ),
            description='When Mode is "add", success response will be like this',
            examples=[
                OpenApiExample(
                    "Success",
                    value={
                        "id": 221,
                        "item_uuid": "4ee5da0c-3ee7-4825-94e6-1756ea4d1e30",
                        "category": "Recommended",
                        "quantity": 1,
                        "cart": 15
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
                name="Exception",
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
    operation_id="add_remove_cart_item",
)
