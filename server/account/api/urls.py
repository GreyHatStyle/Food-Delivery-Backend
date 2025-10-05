from django.urls import include, path

urlpatterns = [
    path("v1/", include("account.api.v1.urls")),
]
