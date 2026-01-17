from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
    inline_serializer,
)
from rest_framework import serializers


create_order_schema_for_docs = extend_schema(
    summary="Create Order",
    description="To create Order of user, when user purchases all the items present in cart",
    request=inline_serializer(
        name="Create Order Body", 
        fields={
            "user_address_id": serializers.IntegerField(help_text="The address id provided by 'User Address' API for particular user"),
            "payment_type": serializers.ChoiceField(
                choices=[
                    ("UPI", "For UPI payments"), 
                    ("CAR", "For Card Payments"),
                    ("COD", "For Cash on Delivery Payments"),
                ]
                ),
            "card_name": serializers.CharField(required=False, help_text="This field should only be used when 'payment_type' is 'CAR', else don't specify this key in json body"),
        }
        ),
    examples=[
        OpenApiExample(
            "Create Order Example",
            summary="Example Order body",
            description="Use this body to test Order Create API",
            value={"user_address_id": 2,"payment_type": "UPI"},
            request_only=True,  # This makes it only show for requests
        ),
    ],
    responses={
        200: OpenApiResponse(
            response=inline_serializer(
                name="CreateOrderResponse",
                fields={
                    "status": serializers.CharField(),
                    "message": serializers.CharField(),
                },
            ),
            description="Order will be created automatically by viewing the current 'Cart' items of User",
            examples=[
                OpenApiExample(
                    "Success",
                    value={
                        "status": "success",
                        "message": "Order created with Order-id: 18 successfully!!"
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
        404: OpenApiResponse(
            response=inline_serializer(
                name="AddressNotFound",
                fields={
                    "status": serializers.CharField(),
                    "message": serializers.CharField(),
                },
            ),
            description="If wrong user's Address id is given",
            examples=[
                OpenApiExample(
                    "Authentication Failed",
                    value={
                    "status": "error",
                    "message": "Invalid following address for user test1 doesn't exists"
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
    tags=["payment"],
    operation_id="create_order",
)
