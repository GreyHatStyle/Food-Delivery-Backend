from rest_framework import generics, permissions, viewsets, response, status
from restaurants.models import Cart, CartItems
from ..serializers import CartSerializer, CartItemSerializer
from utils import print_green, api_exception_handler

class CartAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartSerializer
    pagination_class = None
    # queryset = Cart.objects.prefetch_related("c_items")
    
    def get_object(self):
        """
        Basically if User's cart exists, then show the items, otherwise make one to store items afterwards
        """
        try:
            cart = Cart.objects.prefetch_related("c_items").get(user=self.request.user)
            return cart
        
        except Cart.DoesNotExist:
            return Cart.objects.create(user=self.request.user)
        
        
class CartItemAPI(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartItemSerializer
    pagination_class = None
    queryset = CartItems.objects.all()
    
    def get_queryset(self):
        user = self.request.user
        cart, created = Cart.objects.get_or_create(user=user)
        
        return CartItems.objects.filter(cart=cart)
    
    
    # Overriding this because it gives no response
    @api_exception_handler
    def destroy(self, request, *args, **kwargs):
        cart_id = kwargs['pk']
        print_green(f"Request header: {cart_id}")

        instance = self.get_object()
        self.perform_destroy(instance)
        
        return response.Response({
            "status": "success",
            "result": f"Cart Item {cart_id} has been deleted!!",            
        },status=status.HTTP_204_NO_CONTENT)
        
    
    