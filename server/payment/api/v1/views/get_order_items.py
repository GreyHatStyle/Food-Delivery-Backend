from rest_framework import permissions, views, response, status
from ..serializer import OrderItemsSerializer
from restaurants.models import OrderItems, Order
from utils import api_exception_handler

class GetUserOrderItems(views.APIView):
    """
    Returns validated OrderItems for `order_id` given by user.
    """
    permission_classes = [permissions.IsAuthenticated]

    @api_exception_handler
    def get(self, request, order_id):
        # (Secure Verification) Did this verification, so that any other user won't be able to access
        # other user's order items and details, even after knowing their order primary key 
        
        user_order = Order.objects.filter(user=request.user)
        verified_order_id = None
        for order in user_order:
            if order.pk == order_id:
                verified_order_id = str(order.pk)
                break
        
        
        
        order_items = OrderItems.objects.filter(order=verified_order_id)
        
        serializer = OrderItemsSerializer(order_items, many=True)
        
        return response.Response({
            "status": "success",
            "message": f"Order Items found for user {request.user.username}",
            "results": serializer.data,
        }, status=status.HTTP_200_OK)