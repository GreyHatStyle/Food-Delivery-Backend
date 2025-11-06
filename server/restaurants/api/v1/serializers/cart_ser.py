from rest_framework import serializers
from restaurants.models import Cart, CartItems, Menu
from utils import print_blue, print_green
from decimal import Decimal
from pprint import pprint
from typing import TypedDict


class CartItemType(TypedDict):
    item_uuid: str
    category: str
    quantity: int
    cart_id: int


# TODO: CHANGE WHOLE ARCHITECTURE OF CART ITEMS TO DEAL WITH ONLY MENU_ITEM_ID OF MONGO DB
class CartItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    # Did this because I only needed restaurant_id to by pass serializer validation and arrive in "validation_data", not show in response (since it can't)
    restaurant_id = serializers.CharField(write_only=True) 
    mode = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = CartItems
        fields = [
            'restaurant_id',
            'mode',
            
            
            'id',
            'item_uuid',
            'category',
            'quantity',
            'cart',
        ]
        
        

    def data_in_mongoDB(self, validated_data):
        """
        pipeline to check if incoming data actually exists in mongoDB or not.
        """
        
        pipeline = [
            {
                "$match": {
                    "restaurant_id": validated_data.get("restaurant_id"),
                }
            },
            {
                "$unwind": "$categories",
            },
            {
                "$match": {
                    "categories.name": validated_data.get("category")
                }
            },
            {
                "$unwind": "$categories.menu_items",
            },
            {
                "$match": {
                    "categories.menu_items.item_uuid": validated_data.get("item_uuid")
                },
            },
            {
                "$limit": 1,
            }
        ]
        pprint(pipeline)
        result = Menu.objects.aggregate(pipeline)
        
        verified_item = list(result)
        print_blue(f"Verified Item: {verified_item}")
        # print(verified_item)
        
        if verified_item:
            return verified_item[0]
        
        return None
        
    
    
    def item_already_exists(self, formatted_data: CartItemType) -> CartItems | None:
        """
        To check if data exists in postgreSQL return it
        """
        try:
            item = CartItems.objects.get(
                cart = formatted_data["cart_id"],
                category = formatted_data['category'],
                item_uuid = formatted_data['item_uuid'],
            )
            
            return item
        
        except CartItems.DoesNotExist:
            return None
        
    
    def convert_to_required_db_format(self, data_from_mongoDb, validated_data) -> CartItemType:
        """
        Basically a middle man to convert the data received from mongo db pipeline and validated_data to format required by **PostgreSQL**
        """
        print_green(f"VALIDATED DATA: {validated_data}")
        item_dct: CartItemType = {
            'item_uuid' : data_from_mongoDb['categories']['menu_items']['item_uuid'],
            'category' : data_from_mongoDb['categories']['name'],
            'quantity' : int(validated_data.get("quantity")),
            'cart_id' : validated_data.get("cart").pk,
        }
        
        return item_dct
        
        
    def create(self, validated_data):
        """
        Before creating check if it even exists in mongodb or not, and if it does then check if its exists in postgresql\n
        and then only create data
        """
        
        data_from_mongo = self.data_in_mongoDB(validated_data)
        print_blue(f"Data from mongo: {data_from_mongo}")
        
        
        if not data_from_mongo:
            raise ValueError("Data Not Found in MongoDB, check for any type or spelling mistake")
        
        
        formatted_data = self.convert_to_required_db_format(data_from_mongo, validated_data)
        print_green(f"Formatted data: {formatted_data}")
        
        data_from_postgre: CartItems | None = self.item_already_exists(formatted_data)
        
        mode = validated_data.pop("mode", None)
        
        if data_from_postgre and not mode:
            raise ValueError("Data Already exists!! please provide 'mode' key with either 'add' or 'remove' value, to increase or decrease quantity")
                
        
        validated_data.pop('restaurant_id')
        
        if data_from_postgre:
            if mode == "add":
                data_from_postgre.quantity += 1
                data_from_postgre.save()
        
            
            elif mode == "remove" and data_from_postgre.quantity>0:
                data_from_postgre.quantity -= 1
                
                if data_from_postgre.quantity == 0:
                    data_from_postgre.delete(keep_parents=True)
                    return data_from_postgre
                    
                data_from_postgre.save()
                
            return data_from_postgre
            

        # Now finally create a new data
        
        return super().create(formatted_data)
        


class CartSerializer(serializers.ModelSerializer):
    c_items = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField(default=0)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cart_data_cache = None
    
    class Meta:
        model = Cart
        fields = (
            "id",
            "user",
            'total_quantity',
            'total_items',
            'total_price',
            'c_items',
        )
        
        read_only_fields = ("user", "total_items",)
        
        
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
        
        restaurant_id = str(self.context.get("restaurant_id"))
        print_green(f"context: {self.context}")
        
        item_uuids = []
        quantities = []
        
        for item in cart_items:
            item_uuids.append(item.item_uuid)
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
        for cart_item, quantity in zip(result, quantities):
            cart_item['quantity'] = quantity
            total_price += (cart_item['item_data']['price'] * quantity)
        
        
        self._cart_data_cache = (result, total_price)
        return self._cart_data_cache
    
    
    def get_c_items(self, obj:Cart):
        result, _ = self._get_menu_item_and_cache_it(obj)
        return result
    
    def get_total_price(self, obj:Cart):
        _, total_price = self._get_menu_item_and_cache_it(obj)
        return total_price
        
        