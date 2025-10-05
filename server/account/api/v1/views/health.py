# Create your views here.
from rest_framework import permissions, response, status, views

from ..docs import health_schema
from ._base import api_exception_handler, logger


class HealthAPI(views.APIView):

    logger = logger
    permission_classes = [permissions.AllowAny]

    @health_schema
    @api_exception_handler
    def get(self, request):

        self.logger.info("This api ran fine!!!")
        self.logger.error("Although i want to send error also bruh")

        return response.Response(
            {
                "status": "success",
                "message": "Api working fine",
            },
            status=status.HTTP_200_OK,
        )
