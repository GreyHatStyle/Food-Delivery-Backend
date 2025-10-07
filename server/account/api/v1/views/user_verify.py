from rest_framework import response, status, views
from rest_framework.permissions import IsAuthenticated
from utils import api_exception_handler

from ..docs import user_verify_schema
from ._base import logger


class UserVerifyAPI(views.APIView):
    permission_classes = [IsAuthenticated]
    logger = logger

    @user_verify_schema
    @api_exception_handler
    def get(self, request):

        user = request.user

        print("user object: ", user)

        return response.Response(
            {
                "status": "success",
                "message": f"{user.username} is given",
            },
            status=status.HTTP_200_OK,
        )
