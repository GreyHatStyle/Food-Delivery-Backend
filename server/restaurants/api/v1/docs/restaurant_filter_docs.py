from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
    inline_serializer,
)
from rest_framework import serializers
from ..serializers import RestaurantSerializer

restaurants_filter_schema = extend_schema(
    summary="Filter Restaurants",
    description="Names of all cities whose restaurant are registered in database.",
    auth=[],
    responses={
        200: OpenApiResponse(
            response=inline_serializer(
                name="RestaurantListResponse",
                fields={
                    "status": serializers.ChoiceField(["success", "exception",]),
                    "count": serializers.IntegerField(),
                    "next": serializers.URLField(allow_null=True),
                    "previous": serializers.URLField(allow_null=True),
                    "results": RestaurantSerializer(many=True),
                },
            ),
            description="Displays all available restaurants as per query string",
            examples=[
                OpenApiExample(
                    "Success",
                    value={
                        "id": "963143a1-1d0f-4b88-8f5d-6c94d2601246",
                        "r_name": "Capsicum",
                        "rating": "4.00",
                        "avg_cost": "250.00",
                        "rating_count_str": "5K+ ratings",
                        "cuisine": [
                            "North Indian",
                            "Pizzas"
                        ],
                        "menu_image": "https://fra.cloud.appwrite.io/v1/storage/buckets/68db9320002150bd6130/files/b5515d61-f203-4ba6-81d8-3e694c8a1cf3/view?project=68dad5db002a710b59a4",
                        "r_image_url": None,
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
    operation_id="restaurants_filter",
)

