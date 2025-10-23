from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, pagination, response, status, views
from restaurants.models import Restaurant
from utils import api_exception_handler
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from ..serializers import RestaurantSerializer
from ..filters import GetAllRestaurantsFilter


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
    Get Limited information about all restaurants, for Restaurant cards in frontend.\n
    Supports URL param filtering
    """

    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = GetAllRestaurantsFilter
    ordering_fields = ("rating", "rating_count_int")

    pagination_class = pagination.LimitOffsetPagination

    # Took help from: https://www.cdrf.co/3.16/rest_framework.generics/ListAPIView.html
    @api_exception_handler
    # @method_decorator(cache_page(60 * 5, key_prefix="restaurants_list"))
    def list(self, request, *args, **kwargs):
        """
        Did this to add my response attributes also in future if needed.
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)

            # paginated_response.data["status"] = "success"

            # Did it just to get "success" as first attribute (because success should be first priority!!)
            new_response = {
                "status": "success",
                **(paginated_response.data),
            }

            paginated_response.data = new_response
            return paginated_response

        serializer = self.get_serializer(queryset, many=True)
        return response.Response(
            {
                "status": "success",
                "results": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
