from rest_framework import serializers
from restaurants.models import CartItems, Menu
from utils import print_blue, print_green
from pprint import pprint
from typing import TypedDict


class CartItemType(TypedDict):
    item_uuid: str
    category: str
    quantity: int
    cart_id: int


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
            'quantity' : int(validated_data.get("quantity", "1")),
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
        