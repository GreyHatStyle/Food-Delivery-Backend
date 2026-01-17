from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
    inline_serializer,
)
from rest_framework import serializers

get_all_user_orders_schema = extend_schema(
    summary="Get All User Orders",
    description="To get all past Orders of User, sequenced from latest to first order. It supports Limit-Offset Pagination",
    request=inline_serializer(name="UserAllOrders", fields={}),
    responses={
        200: OpenApiResponse(
            response=inline_serializer(
                name="SuccessResponse",
                fields={
                    "count": serializers.IntegerField(),
                    "next": serializers.CharField(),
                    "previous": serializers.CharField(),
                    "results": serializers.ListField()  
                },
            ),
            description="If everything went right",
            examples=[
                OpenApiExample(
                    "Success",
                    value={
                        "id": 18,
                        "restaurant_img": "Image stored URL of cloud",
                        "restaurant_name": "Paprika Food Court",
                        "item_list": [
                            {
                                "name": "Veg Fried Rice + Chilli Paneer Gravy",
                                "quantity": 1,
                                "price": 250.0,
                                "veg": True
                            }
                        ],
                        "service_charges": {
                            "delivery_fee": 27.0,
                            "gst_fee": 25.99
                        },
                        "created_at": "2026-01-17T15:55:15.777236+05:30",
                        "status": "DEL",
                        "delivery_address": "A-301, Great Society, Citynagar, Statepradesh, 282828.",
                        "payment_type": "UPI",
                        "card_name": None,
                        "restaurant": "3637f7d6-a435-41bf-bdff-f3459004e690"
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
    operation_id="get_all_user_orders",
)
