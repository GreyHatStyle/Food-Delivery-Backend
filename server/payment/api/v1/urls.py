from django.urls import path

from . import views

urlpatterns = [
    path("order/", views.CreateOrderFromCartAPI.as_view(), name="order-from-cart"),
    path("order/<int:order_id>", views.GetUserSingleOrderAPI.as_view(), name="order-id-get"),
    path("order/all/", views.GetUserOrdersAPI.as_view(), name="order-all-get"),
]