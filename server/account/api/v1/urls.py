from django.urls import path

from . import views

urlpatterns = [
    path("health/", views.HealthAPI.as_view(), name="health-api"),
    path("user/", views.UserVerifyAPI.as_view(), name="user-verify-api"),
    path("login/", views.LoginAPI.as_view(), name="login-api"),
]
