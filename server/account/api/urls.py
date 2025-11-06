from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("v1/", include("account.api.v1.urls")),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
