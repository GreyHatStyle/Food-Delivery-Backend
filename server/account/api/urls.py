from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView
from .v1.docs import refresh_token_schema


@refresh_token_schema
class CustomTokenRefreshView(TokenRefreshView):
    # Did this so that it can appear well in Scalar API Docs
    pass


urlpatterns = [
    path("v1/", include("account.api.v1.urls")),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]
