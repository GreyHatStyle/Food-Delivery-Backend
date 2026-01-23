from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
    inline_serializer,
)
from rest_framework import serializers

cart_get_schema = extend_schema(
    summary="Get Cart Details",
    description="Provides details related to items that user put in cart, the restaurant details of items, all stored in root server. This is done so that cart information can be provided and updated in frontend even if person is logged in on different device",
    request=inline_serializer(name="CartDetails", fields={}),
    responses={
        200: OpenApiResponse(
            response=inline_serializer(
                name="SuccessResponse",
                fields={
                    "status": serializers.ChoiceField(["success", "error", "exception",]),
                    "results": inline_serializer(
                        name="results",
                        fields={
                            "id": serializers.IntegerField(),
                            "user": serializers.CharField(),
                            "restaurant": serializers.CharField(),
                            "total_quantity": serializers.IntegerField(),
                            "total_items": serializers.IntegerField(),
                            "total_price": serializers.FloatField(),
                            "c_items": serializers.ListField(),
                            "restuarant_name": serializers.CharField(),
                            "service_charges": inline_serializer(
                                name="ServiceCharges",
                                fields={
                                    "delivery_fee": serializers.FloatField(),
                                    "gst_fee": serializers.FloatField(),
                                },
                            ),
                            "to_pay": serializers.FloatField(),
                        }
                    ),
                },
            ),
            description="Display's cart items and their restaurant details with total cost and service charges.",
            examples=[
                OpenApiExample(
                    "Success",
                    value={
                        "status": "success",
                        "results": {
                            "id": 16,
                            "user": "bef693e3-43f0-485e...",
                            "restaurant": "3637f7d6-a435-...",
                            "total_quantity": 1,
                            "total_items": 1,
                            "total_price": 250.0,
                            "c_items": [
                                {
                                    "category_name": "Recommended",
                                    "item_data": {
                                        "item_uuid": "e0a1bd21-f86c-...",
                                        "name": "Veg Fried Rice + Chilli Paneer Gravy",
                                        "price": 250.0,
                                        "food_type": "V",
                                        "image_url": "image_cloud_url"
                                    },
                                    "quantity": 1,
                                    "cart_item_id": 220
                                }
                            ],
                            "restaurant_name": "Paprika Food Court",
                            "service_charges": {
                                "delivery_fee": 27.0,
                                "gst_fee": 25.99
                            },
                            "to_pay": 302.99
                        }
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
    operation_id="cart_manage_get",
)

