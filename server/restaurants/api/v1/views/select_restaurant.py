from rest_framework import views, response, status
from restaurants.models import Restaurant
from ..serializers import MenuSerializer
from django.db import connection
from logging import getLogger
from utils import api_exception_handler


class OpenRestaurantAPI(views.APIView):

    logger = getLogger("restaurants")

    @api_exception_handler
    def get(self, request, restaurant_id, category=None):

        restaurants = Restaurant.objects.filter(id=restaurant_id)
        serializer = MenuSerializer(restaurants, many=True, category=category)

        self.logger.debug("Query executed: ", connection.queries)

        return response.Response(
            {
                "status": "success",
                "results": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
