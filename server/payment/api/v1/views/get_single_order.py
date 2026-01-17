from rest_framework import permissions, pagination, response, status
from rest_framework.generics import RetrieveAPIView
from ..serializer import OrderSerializer
from restaurants.models import Order, Restaurant
from utils import api_exception_handler

from ..docs import get_single_user_orders_schema


# class GetUserOrderItems(views.APIView):
#     """
#     Returns validated OrderItems for `order_id` given by user.
#     """
#     permission_classes = [permissions.IsAuthenticated]

#     @api_exception_handler
#     def get(self, request, order_id):
#         # (Secure Verification) Did this verification, so that any other user won't be able to access
#         # other user's order items and details, even after knowing their order primary key 
        
#         try:
#             user_order = Order.objects.get(user=request.user, id=order_id)
        
#         except Order.DoesNotExist:
#             return response.Response({
#                 "status": "error",
#                 "message": f"Orders for user {request.user.username}, with this order id {order_id} doesn't exist",
#             }, status=status.HTTP_404_NOT_FOUND)    
            
        
        
        
#         order_items = OrderItems.objects.filter(order=user_order)
        
#         serializer = OrderItemsSerializer(order_items, many=True)
        
#         return response.Response({
#             "status": "success",
#             "message": f"Order Items found for user {request.user.username}",
#             "results": serializer.data,
#         }, status=status.HTTP_200_OK)
        
        
        
class GetUserSingleOrderAPI(RetrieveAPIView):
    """
    (RetrieveAPIView)
    Returns validated Order and its items for `order_id` given by user.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer
    pagination_class = pagination.LimitOffsetPagination
    lookup_url_kwarg = 'order_id'
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')
    
    def handle_exception(self, exc):
        response_ = super().handle_exception(exc)
        # print("Kwargs: ", self.kwargs)
        if response_ is not None:
            custom_response = {
                "status": "error",
                # "message": response_.data.get('detail', str(exc))
                "message": f"Orders for user {self.request.user.username}, with this order id {self.kwargs['order_id']} doesn't exist"
            }
            response_.data = custom_response
            response_.status_code = status.HTTP_403_FORBIDDEN
        
        return response_
    
    # @api_exception_handler
    def retrieve(self, request, *args, **kwargs):
        
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        restaurant = Restaurant.objects.only("address").get(id=serializer.data.get("restaurant"))
        print("Restaurant: ", restaurant)
        
        return response.Response({
            "status": "success",
            "message": "Found order details!!",
            "order": serializer.data,
            "restaurant_address": restaurant.address,
        }, status=status.HTTP_200_OK)
        
        
    @get_single_user_orders_schema
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
