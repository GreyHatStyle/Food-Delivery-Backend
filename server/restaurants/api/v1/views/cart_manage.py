from rest_framework import generics, permissions, viewsets, response, status
from restaurants.models import Cart, CartItems
from ..serializers import CartSerializer, CartItemSerializer
from utils import print_green, api_exception_handler
# from django.utils.decorators import method_decorator
# from django.views.decorators.cache import cache_page
# from django.views.decorators.vary import vary_on_headers


class CartAPI(generics.RetrieveAPIView):
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
        
    @api_exception_handler
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return response.Response({
            "status": "success",
            "results": serializer.data,
        })
        

        
class CartItemAPI(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartItemSerializer
    pagination_class = None
    queryset = CartItems.objects.all()
    
    def get_queryset(self):
        """
        This will ensure user can do changes in their cart only
        """
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
        
    
    @api_exception_handler
    def create(self, request, *args, **kwargs):
        """
        Will take out user's id and find its one-to-one cart, and then return it to serializer, to avoid any user updating anyone's cart.\n
        Also frontend won't need to send user's cart id now.
        """
        user = request.user
        cart_id = Cart.objects.only('id').get(user=user).pk
        
        print_green("Request data")
        
        request.data['cart'] = cart_id
        print(request.data)
        
        return super().create(request, *args, **kwargs)
        
    def list(self, request, *args, **kwargs):
        return response.Response({
            "status": "error",
            "reason": "This request is removed and can't be fulfilled please use the Get Cart request only to get all cart items",
        }, status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, *args, **kwargs):
        return response.Response({
            "status": "error",
            "reason": "This request is removed and can't be fulfilled please use the Post request only to perform actions",
        }, status=status.HTTP_400_BAD_REQUEST)
        
    
    def partial_update(self, request, *args, **kwargs):
        return response.Response({
            "status": "error",
            "reason": "This request is removed and can't be fulfilled please use the Post request only to perform actions",
        }, status=status.HTTP_400_BAD_REQUEST)
    
    