from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
    inline_serializer,
)
from rest_framework import serializers
from ..serializers import RestaurantSerializer, MenuSerializer

one_restaurant_schema = extend_schema(
    summary="One restaurant select",
    description="Names of all cities whose restaurant are registered in database.",
    auth=[],
    responses={
        200: OpenApiResponse(
            response=inline_serializer(
                name="RestaurantDetailResponse",
                fields={
                    "status": serializers.ChoiceField(["success", "exception",]),
                    "results": inline_serializer(
                        name="RestaurantWithMenu",
                        fields={
                            **RestaurantSerializer().fields,
                            "category": inline_serializer(
                                name="AttriName",
                                fields={
                                    "names": serializers.ListField(child=serializers.CharField())
                                }
                            ),
                            "menu_data": MenuSerializer(many=True),
                        }
                    ),
                },
            ),
            description="Displays all restaurant and its menu details of selected restaurant",
            examples=[
                OpenApiExample(
                    "Success",
                    value={
                        "status": "success",
                        "results": [
                            {
                                "id": "3a5f386a-ba45-4aa2-aae3-3cfdb7a536fc",
                                "r_name": "Sutthimani",
                                "rating": "4.10",
                                "avg_cost": "400.00",
                                "rating_count_str": "100+ ratings",
                                "cuisine": [
                                    "Indian",
                                    "South Indian"
                                ],
                                "menu_image": "https://fra.cloud.appwrite.io/v1/storage/buckets/68db9320002150bd6130/files/82c76110-1803-4e81-ad80-8e85948e213e/view?project=68dad5db002a710b59a4",
                                "r_image_url": None,
                                "address": "Sutthimani, 127/123, Hamirpur Rd, Juhi, Kanpur, Uttar Pradesh 208014, India",
                                "category": [
                                    {
                                        "names": [
                                            "Recommended",
                                            "Mini Bites",
                                            "Thali",
                                            "Breakfast",
                                            "South Indian"
                                        ]
                                    }
                                ],
                                "menu_data": [
                                    {
                                        "restaurant_id": "3a5f386a-ba45-4aa2-aae3-3cfdb7a536fc",
                                        "categories": {
                                            "name": "Recommended",
                                            "menu_items": [
                                                {
                                                    "item_uuid": "3df9a3d1-45a7-4e8a-9a0c-46439cd5630a",
                                                    "name": "Karolbagh Ke Chhole Kulche",
                                                    "price": 185.0,
                                                    "food_type": "V",
                                                    "image_url": "https://fra.cloud.appwrite.io/v1/storage/buckets/68db9320002150bd6130/files/82c76110-1803-4e81-ad80-8e85948e213e/view?project=68dad5db002a710b59a4"
                                                },
                                                {
                                                    "item_uuid": "1e54e03b-04b4-4a86-929f-c5b321826db7",
                                                    "name": "Shahi Paneer ( Full )",
                                                    "price": 385.0,
                                                    "food_type": "V",
                                                    "image_url": "https://fra.cloud.appwrite.io/v1/storage/buckets/68db9320002150bd6130/files/5ad136b4-f610-4898-b067-1a062945f966/view?project=68dad5db002a710b59a4"
                                                }
                                            ]
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                    ,
                ),
                
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
    operation_id="restaurants_open",
)

