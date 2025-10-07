from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, pagination, response, status, views
from restaurants.models import Restaurant
from utils import api_exception_handler

from ..serializers import RestaurantSerializer


class GetCitiesNames(views.APIView):
    """
    Will provide list of unique cities for frontend homepage.
    """

    @api_exception_handler
    def get(self, request):
        city_queryset = Restaurant.objects.values("city").distinct()
        cities = [item["city"] for item in city_queryset]

        return response.Response(
            {
                "status": "success",
                "cities": cities,
            },
            status=status.HTTP_200_OK,
        )


class GetAllRestaurants(generics.ListAPIView):
    """
    Get Limited information about all restaurants, for Restaurant cards in frontend.
    """

    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("city",)
    ordering_fields = ("rating", "rating_count_int")
    pagination_class = pagination.LimitOffsetPagination
