from django.contrib.auth import authenticate
from rest_framework import response, status, views
from rest_framework_simplejwt.tokens import RefreshToken
from utils import api_exception_handler

from ..docs import login_schema_for_docs
from ..serializers import LoginValidation, UserSerializer
from ._base import logger


class LoginAPI(views.APIView):
    """
    API class to help user to login, and obtain JWT access and refresh tokens.
    """

    logger = logger

    @login_schema_for_docs
    @api_exception_handler
    def post(self, request):

        validation_serializer = LoginValidation(data=request.data)

        if not validation_serializer.is_valid():
            return response.Response(
                {
                    "status": "failed",
                    "message": validation_serializer.show_first_error(),
                    "errors": validation_serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        validated_data = validation_serializer.validated_data

        user = None

        if isinstance(validated_data, dict):
            user = authenticate(
                username=validated_data["username"],
                password=validated_data["password"],
            )

        attempts_left = 3

        if user:
            refresh = RefreshToken.for_user(user=user)
            serializer = UserSerializer(user)

            return response.Response(
                {
                    "status": "success",
                    "message": "Logged in successfully!!",
                    "user": serializer.data,
                    "tokens": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                },
                status=status.HTTP_200_OK,
            )

        return response.Response(
            {
                "status": "failed",
                "message": f"Username or Password is Incorrect,"
                f" {attempts_left} {"attempts" if attempts_left > 1 else "attempt"} left",
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )
