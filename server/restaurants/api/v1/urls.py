from django.urls import path

from . import views

urlpatterns = [
    path("restaurants/", views.GetAllRestaurants().as_view(), name="restaurants"),
    path("cities/", views.GetCitiesNames().as_view(), name="unique-cities"),
]
