from django.urls import path

from . import views

urlpatterns = [
    path("restaurants/", views.GetAllRestaurants().as_view(), name="restaurants"),
    path(
        "restaurants/<uuid:restaurant_id>/",
        views.OpenRestaurantAPI().as_view(),
        name="restaurants-id",
    ),
    path(
        "restaurants/<uuid:restaurant_id>/<str:category>",
        views.OpenRestaurantAPI().as_view(),
        name="restaurants-id-category",
    ),
    path("cities/", views.GetCitiesNames().as_view(), name="unique-cities"),
]
