from rest_framework import views, permissions, viewsets, response, status
from restaurants.models import Cart, CartItems, Restaurant
from ..serializers import CartSerializer, CartItemSerializer
from utils import print_green, api_exception_handler
from uuid import UUID
from ..docs import cart_get_schema, cart_delete_schema, add_remove_cart_item_schema, delete_cart_item_schema


class CartAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartSerializer
    pagination_class = None
    # queryset = Cart.objects.prefetch_related("c_items")
    
    @cart_get_schema
    @api_exception_handler
    def get(self, request):
        
        try:
            cart= Cart.objects.get(user=request.user)
            serializer = CartSerializer(
                cart,
                # context = {
                #     "restaurant_id": restaurant_id,
                # }
            )
            
            
            return response.Response({
                "status": "success",
                "results": serializer.data,
                
            }, status=status.HTTP_200_OK)
            
        except Cart.DoesNotExist:
            return response.Response({
                "status": "error",
                "message": "Cart of this user's name doesn't exists!!",
            }, status=status.HTTP_400_BAD_REQUEST)
            
         
    @cart_delete_schema
    @api_exception_handler
    def delete(self, request):
        """
        Clear Cart API
        """
        try:
            cart= Cart.objects.get(user=request.user)
            cart_id = cart.pk
            cart_items = CartItems.objects.filter(cart_id=cart_id).prefetch_related()
            cart_items.delete()
           
            return response.Response({
                "status": "success",
                "message": f"Cart with {cart_id} of user {request.user.username} has been deleted",
                
            }, status=status.HTTP_204_NO_CONTENT)
            
        except Cart.DoesNotExist:
            return response.Response({
                "status": "error",
                "message": "Cart of this user's name doesn't exists!!",
            }, status=status.HTTP_400_BAD_REQUEST)
        

        
class CartItemAPI(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartItemSerializer
    pagination_class = None
    queryset = CartItems.objects.all()
    http_method_names = ['post', 'delete', 'head', 'options']
    
    def get_queryset(self):
        """
        This will ensure user can do changes in their cart only
        """
        user = self.request.user
        cart, created = Cart.objects.get_or_create(user=user)
        
        return CartItems.objects.filter(cart=cart)
    
    def handle_exception(self, exc):
        response_ = super().handle_exception(exc)
        # print("Kwargs: ", self.kwargs)
        if response_ is not None:
            custom_response = {
                "status": "error",
                "message": f"Cart Item for user {self.request.user.username}, with this Id {self.kwargs['pk']} doesn't exist"
            }
            response_.data = custom_response
            response_.status_code = status.HTTP_403_FORBIDDEN
        
        return response_
    
    
    # Overriding this because it gives no response
    @delete_cart_item_schema
    def destroy(self, request, *args, **kwargs):
        cart_id = kwargs['pk']
        print_green(f"Request header: {cart_id}")

        instance = self.get_object()
        self.perform_destroy(instance)
        
        return response.Response({
            "status": "success",
            "result": f"Cart Item {cart_id} has been deleted!!",            
        },status=status.HTTP_204_NO_CONTENT)
        
    
    @add_remove_cart_item_schema
    @api_exception_handler
    def create(self, request, *args, **kwargs):
        """
        Will take out user's id and find its one-to-one cart, and then return it to serializer, to avoid any user updating anyone's cart.\n
        Also frontend won't need to send user's cart id now.
        """
        user = request.user
        restaurant_id = request.data.get("restaurant_id")
        
        restaurant = Restaurant.objects.only('id').get(id=UUID(restaurant_id))
        
        try:
            cart = Cart.objects.only('id', 'restaurant_id').get(user=user)
            
            # User is ordering from different restaurant, delete all cart items
            if cart.restaurant != restaurant:
                CartItems.objects.filter(cart=cart).delete()
                cart.restaurant = restaurant
                cart.save()
                
        except Cart.DoesNotExist:
            
            # So user is adding first time in cart
            cart = Cart.objects.create(
                user=user,
                restaurant=restaurant,    
            )
            
        
        
        # I know I am gonna confuse in it in future, so even though I am sending cart object's primary key
        # Here, it in serializer's create() method's 'validated_data', it will have cart's object only
        request.data['cart'] = cart.pk
        print(request.data)
        
        return super().create(request, *args, **kwargs)
        
    # REMOVING THIS FOR NOW BECAUSE I COULD HAVE ACHIEVED THIS USING 'http_method_names' ATTRIBUTE IN CLASS VARIABLE :)
    
    # def list(self, request, *args, **kwargs):
    #     return response.Response({
    #         "status": "error",
    #         "reason": "This request is removed and can't be fulfilled please use the Get Cart request only to get all cart items",
    #     }, status=status.HTTP_403_FORBIDDEN)
        
    # def update(self, request, *args, **kwargs):
    #     return response.Response({
    #         "status": "error",
    #         "reason": "This request is removed and can't be fulfilled please use the Post request only to perform actions",
    #     }, status=status.HTTP_400_BAD_REQUEST)
        
    
    # def partial_update(self, request, *args, **kwargs):
    #     return response.Response({
    #         "status": "error",
    #         "reason": "This request is removed and can't be fulfilled please use the Post request only to perform actions",
    #     }, status=status.HTTP_400_BAD_REQUEST)
    
    
