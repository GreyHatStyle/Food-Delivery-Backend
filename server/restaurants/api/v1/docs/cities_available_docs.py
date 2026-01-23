from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
    inline_serializer,
)
from rest_framework import serializers

cities_get_schema = extend_schema(
    summary="Get City Names",
    description="Names of all cities whose restaurant are registered in database.",
    auth=[],
    responses={
        200: OpenApiResponse(
            response=inline_serializer(
                name="SuccessResponse",
                fields={
                    "status": serializers.ChoiceField(["success", "exception",]),
                    "cities": serializers.ListField(
                        child=serializers.CharField()    
                    ),
                },
            ),
            description="Displays all cities whose restaurant is available",
            examples=[
                OpenApiExample(
                    "Success",
                    value={
                        "status": "success",
                        "cities": [
                            "Bikaner",
                            "Varanasi",
                            "Noida-1",
                            "Patna",
                            "Faridabad",
                            "Kanpur"
                        ]
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
    operation_id="get_cities",
)

