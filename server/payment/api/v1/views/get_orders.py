from rest_framework.generics import ListAPIView
from rest_framework import response, permissions, status, pagination
from ..serializer import OrderSerializer
from restaurants.models import Order

class GetUserOrdersAPI(ListAPIView):
    """
    Returns all the order details for Required User
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer
    pagination_class = pagination.LimitOffsetPagination
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
        
