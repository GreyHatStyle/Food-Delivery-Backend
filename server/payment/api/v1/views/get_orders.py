from rest_framework.generics import ListAPIView
from rest_framework import permissions, pagination
from ..serializer import OrderSerializer
from restaurants.models import Order

from ..docs import get_all_user_orders_schema

class GetUserOrdersAPI(ListAPIView):
    """
    (ListAPIView)
    Returns all the order details for Required User
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer
    pagination_class = pagination.LimitOffsetPagination
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')
    
    @get_all_user_orders_schema
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
        
