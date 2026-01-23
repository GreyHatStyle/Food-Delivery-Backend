from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
    inline_serializer,
)
from rest_framework import serializers

get_single_user_orders_schema = extend_schema(
    summary="Get Single Order Details",
    description="To get All details for single order, by using it's order id.",
    request=inline_serializer(name="UserGetOrder", fields={}),
    responses={
        200: OpenApiResponse(
            response=inline_serializer(
                name="SuccessResponse",
                fields={
                    "status": serializers.ChoiceField(["success", "error", "exception",]),
                    "message": serializers.CharField(),
                    "order": inline_serializer(
                        name="OrderDetails",
                        fields={
                            "id": serializers.IntegerField(),
                            "restaurant_img": serializers.CharField(),
                            "restaurant_name": serializers.CharField(),
                            "item_list": serializers.ListField(),
                            "service_charges": inline_serializer(
                                name="ServiceCharges",
                                fields={
                                    "delivery_fee": serializers.IntegerField(),
                                    "gst_fee": serializers.IntegerField(),
                                }
                            ),
                            "created_at": serializers.CharField(),
                            "status": serializers.ChoiceField(choices=["DEL", "CAN", "PEN"]),
                            "delivery_address": serializers.CharField(),
                            "payment_type": serializers.ChoiceField(choices=["UPI", "CAR", "COD"]),
                            "card_name": serializers.CharField(required=False),
                            "restaurant": serializers.CharField(), 
                        }
                    ),
                    "restaurant_address": serializers.CharField(),
                },
            ),
            description="Shows All required details of a order, like restaurant, service charges, etc",
            examples=[
                OpenApiExample(
                    "Success",
                    value={
                        "status": "success",
                        "message": "Found order details!!",
                        "order": {
                            "id": 1,
                            "restaurant_img": "restaurant image saved in cloud URL",
                            "restaurant_name": "JSB EVERGREEN SNACKS & SWEETS",
                            "item_list": [
                                {
                                    "name": "Chole Bhature With Lassi",
                                    "quantity": 1,
                                    "price": 150.0,
                                    "veg": True,
                                }
                            ],
                            "service_charges": {
                                "delivery_fee": 27.0,
                                "gst_fee": 25.99
                            },
                            "created_at": "2025-12-29T07:50:46.479921+05:30",
                            "status": "DEL",
                            "delivery_address": "A-301, Great Society, Citynagar, Statepradesh, 282828.",
                            "payment_type": "UPI",
                            "card_name": None,
                            "restaurant": "7eb6e4ec-8415-463d-a314-994f7f8b3615"
                        },
                        "restaurant_address": "JSB EVERGREEN SNACKS & SWEETS, MAIN MARKET BRAHMAPUTRA SHOPPING COMPLEX SECTOR, DISTRICT, GAUTAM BUDDHA NAGAR UTTAR PRADESH  201301"
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
        403: OpenApiResponse(
            response=inline_serializer(
                name="AccessingSomeoneElseError",
                fields={
                    "status": serializers.CharField(),
                    "message": serializers.CharField(),
                },
            ),
            description="If user 'test1' tries to access someone else order id, (even if he knows their order id), server will forbid it securing another user's order details from 'test1' user",
            examples=[
                OpenApiExample(
                    "Authentication Failed",
                    value={
                        "status": "error",
                        "message": "Orders for user test1, with this order id 1 doesn't exist"
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
    operation_id="get_single_user_order_details",
)
