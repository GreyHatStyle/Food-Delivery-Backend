from rest_framework import serializers
from restaurants.models import Cart, Menu
from utils import print_green
from typing import TypedDict, List

class CartItemType(TypedDict):
    item_uuid: str
    item_id: int
    quantity: int

class CartSerializer(serializers.ModelSerializer):
    c_items = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField(default=0)
    restaurant_name = serializers.SerializerMethodField()
    service_charges = serializers.SerializerMethodField()
    to_pay = serializers.SerializerMethodField()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cart_data_cache = None
        # self.total_item_stored_price = None
        self.price_to_pay = 0
    
    class Meta:
        model = Cart
        fields = (
            "id",
            "user",
            'restaurant',
            'total_quantity',
            'total_items',
            'total_price',
            'c_items',
            'restaurant_name',
            'service_charges',
            'to_pay',
        )
        
        read_only_fields = ("user", "total_items", )
        
        
    def _get_menu_item_and_cache_it(self, obj: Cart):
        """
        Get all menu items data from mongoDB, ***inspired from Memorization in Dynamic Programming (DP)***\n
        
        Did this so that We don't have to call mongoDb pipeline 2 times for getting result and calculating price.
        """
        if self._cart_data_cache:
            return self._cart_data_cache
        
        cart_items = obj.c_items.all()
        
        if not cart_items.exists():
            return ([], 0)
        
        restaurant_id = str(obj.restaurant.id)
        print_green(f"context: {self.context}")
        
        item_uuids = []
        
        cart_item_lst: List[CartItemType] = []
        
        for item in cart_items:
            item_uuids.append(item.item_uuid)
            
            cart_item_lst.append({
                "item_id": item.pk,
                "item_uuid": item.item_uuid,
                "quantity": item.quantity,
            })
        
        
        pipe_line = [
            {
                "$match": {
                    "restaurant_id": restaurant_id, 
                }
            },
            {"$unwind": "$categories",},
            {"$unwind": "$categories.menu_items"},
            {
                "$match": {
                    "categories.menu_items.item_uuid": {
                        "$in": item_uuids,
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
        
        items = Menu.objects.aggregate(pipe_line)
        result = list(items)
        
        total_price = 0
        
        
        # FIX: The returned items from mongoDB were not on same order as stored in lists earlier, hence data's id and quantity
        # were mis matching (DB: item_uuid: "fdb.." has 2 quantity, API: item_uuid: "fdb.." has 1 quantity),
        # Fixed it to save and find correct item's data, IN FUTURE NEED TO OPTIMIZE THIS SEARCH PROCESS
        for cart_item in result:
            for item in cart_item_lst:
                if item["item_uuid"] == cart_item['item_data']['item_uuid']:
                    cart_item['quantity'] = item['quantity']
                    cart_item['cart_item_id'] = item["item_id"]
                    total_price += (cart_item['item_data']['price'] * item["quantity"])
                    break
                    
        
        
        self._cart_data_cache = (result, total_price)
        return self._cart_data_cache
    
    
    def get_c_items(self, obj:Cart):
        result, _ = self._get_menu_item_and_cache_it(obj)
        return result
    
    def get_total_price(self, obj:Cart):
        _, total_price = self._get_menu_item_and_cache_it(obj)
        self.price_to_pay += total_price
        return total_price
        
    def get_restaurant_name(self, obj:Cart):
        return obj.restaurant.r_name
        
    def get_service_charges(self, obj:Cart):
        """
        Can Add services charges dynamically in future from here
        """
        services = {
            "delivery_fee": 27.00,
            "gst_fee": 25.99,
        }
        
        for key, price in services.items():
            self.price_to_pay += price
        
        return services
        
    def get_to_pay(self, obj: Cart):
        if self.price_to_pay == 0:
            raise ValueError("Get to pay not set yet")
        
        return self.price_to_pay