from rest_framework import serializers
from restaurants.models import Order, OrderItems, Restaurant
from typing import TypedDict, List

class ItemListType(TypedDict):
    name: str
    quantity: int
    price: float
    veg: bool
class OrderSerializer(serializers.ModelSerializer):
    restaurant_img = serializers.SerializerMethodField()
    restaurant_name = serializers.SerializerMethodField()
    item_list = serializers.SerializerMethodField()
    service_charges = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        exclude = ('user', )
        
    def get_restaurant_img(self, obj: Order):
        order_item = OrderItems.objects.filter(order=obj).first()
        return order_item.image_url
    
    def get_restaurant_name(self, obj: Order):
        restaurant = Restaurant.objects.get(id=obj.restaurant.pk)
        return restaurant.r_name
        
    def get_item_list(self, obj: Order):
        order_item = OrderItems.objects.filter(order=obj)
        items_lst: List[ItemListType] = []
        for item in order_item:
            items_lst.append({
                'name': item.name,
                'quantity': item.quantity,
                'price': item.price,
                'veg': item.veg,
            })
            
        return items_lst
    
    def get_service_charges(self, obj:Order):
        """
        Can Add services charges dynamically in future from here
        """
        services = {
            "delivery_fee": 27.00,
            "gst_fee": 25.99,
        }
        
        return services