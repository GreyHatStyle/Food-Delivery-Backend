from django.urls import include, path

urlpatterns = [
    path("v1/", include("restaurants.api.v1.urls")),
]
