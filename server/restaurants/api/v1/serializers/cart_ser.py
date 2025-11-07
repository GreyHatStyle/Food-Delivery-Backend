from rest_framework import serializers
from restaurants.models import Cart, Menu
from utils import print_green


class CartSerializer(serializers.ModelSerializer):
    c_items = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField(default=0)
    restaurant_name = serializers.SerializerMethodField()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cart_data_cache = None
    
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
        quantities = []
        item_ids = []
        
        for item in cart_items:
            item_uuids.append(item.item_uuid)
            item_ids.append(item.pk)
            quantities.append(item.quantity)
        
        
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
        for cart_item, quantity, pg_id in zip(result, quantities, item_ids):
            cart_item['quantity'] = quantity
            cart_item['cart_item_id'] = pg_id
            total_price += (cart_item['item_data']['price'] * quantity)
        
        
        self._cart_data_cache = (result, total_price)
        return self._cart_data_cache
    
    
    def get_c_items(self, obj:Cart):
        result, _ = self._get_menu_item_and_cache_it(obj)
        return result
    
    def get_total_price(self, obj:Cart):
        _, total_price = self._get_menu_item_and_cache_it(obj)
        return total_price
        
    def get_restaurant_name(self, obj:Cart):
        return obj.restaurant.r_name
        