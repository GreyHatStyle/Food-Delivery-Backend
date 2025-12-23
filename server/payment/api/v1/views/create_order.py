from rest_framework import views, status,response, permissions
from restaurants.models import Cart, CartItems, Order, OrderItems, OrderStatusChoices, PaymentTypeChoices, Menu
from typing import List
from pprint import pprint
from utils import api_exception_handler

from account.models import UserAddress

class CreateOrderFromCartAPI(views.APIView):
    """
    (APIView)
    Uses, user's cart to create order and order's item, ***queries***:
    - First user's data for id.
    - User's address for saving it.
    - User's cart.
    - User's cart item
    - Cart from restaurant.
    """
    
    permission_classes = [permissions.IsAuthenticated]
    
    @api_exception_handler
    def post(self, request):
        user = request.user
        user_address_id = request.data.get("user_address_id")
        payment_type = request.data.get("payment_type")
        card_name = request.data.get("card_name")
        
        exists = False
        for pay_type, _ in PaymentTypeChoices.choices:
            if pay_type == payment_type:
                exists = True
                break
            
        if not exists:
            return response.Response({
                "status": "error",
                "message": "Invalid payment TYPE!!",
            }, status=status.HTTP_400_BAD_REQUEST)
            
        
        try:
            user_address = UserAddress.objects.get(
                id = user_address_id,
                user = user
            )
                
        except UserAddress.DoesNotExist:
            return response.Response({
                    "status": "error",
                    "message": f"Invalid following address for user {user.username} doesn't exists",
                }, status=status.HTTP_404_NOT_FOUND)
        
        
        
        cart = Cart.objects.only('id', 'restaurant_id').get(user = user)
        cart_items = CartItems.objects.filter(cart=cart).prefetch_related()
        
        
        final_user_address = f"{user_address.main_address}, {user_address.city}, {user_address.state}, {user_address.pin_code}."
        
        user_order = Order(
            user = request.user,
            restaurant = cart.restaurant,
            status = OrderStatusChoices.DELIVERED,
            delivery_address = final_user_address,
            payment_type = payment_type,
            card_name = card_name,
        )
        user_order.save()
        
        cart_items_uuid: List[str] = []
        for item in cart_items:
            cart_items_uuid.append(item.item_uuid)
        
        print(cart_items_uuid)
        
        mongo_pipeline = [
            {
                "$match": {
                    "restaurant_id": str(cart.restaurant.pk),
                }
            },
            {"$unwind": "$categories"},
            {"$unwind": "$categories.menu_items"},
            {
                "$match": {
                    "categories.menu_items.item_uuid": {
                        "$in": cart_items_uuid
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "category_name": "$categories.name",
                    "item_data": "$categories.menu_items",
                    
                }
            }
        ]
        
        items_from_mongo = list(Menu.objects.aggregate(mongo_pipeline))
        pprint(items_from_mongo)
        
        
        order_items_list: List[OrderItems] = []
        
        # Need to optimize it after wards
        """
        `cart_item` format, example:
        {
            'category_name': 'Recommended',
            'item_data': {
                'food_type': 'NV',
                'image_url': 'image url',
                'item_uuid': '618ae478-uuid-342342342',
                'name': 'Mutton Shami Kebab',
                'price': 130.0
            }
        },
        """
        for cart_item_mongo in items_from_mongo:
            for cart_item in cart_items:
                if cart_item.item_uuid == cart_item_mongo['item_data']['item_uuid']:
                    order_item = OrderItems(
                        order=user_order,
                        name = cart_item_mongo['item_data']['name'],
                        price = cart_item_mongo['item_data']['price'],
                        image_url = cart_item_mongo['item_data']['image_url'],
                        category = cart_item_mongo['category_name'],
                        veg = cart_item_mongo['item_data']['food_type'] == 'V',
                        quantity = cart_item.quantity,
                    )
                    order_items_list.append(order_item)
                    break
        
        
        OrderItems.objects.bulk_create(order_items_list)
        
        return response.Response({
            "status": "success",
            "message": f"Order created with Order-id: {user_order.pk} successfully!!",
        }, status=status.HTTP_200_OK)
        
        