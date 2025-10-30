from rest_framework import serializers
from restaurants.models import Cart, CartItems, Menu
from utils import print_blue
from decimal import Decimal
from pprint import pprint



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
            'name',
            'price',
            'image_url',
            'category',
            'quantity',
            'veg',
            'cart',
        ]
        
        

    def data_in_mongoDB(self, validated_data) -> bool:
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
                    "categories.menu_items.name": validated_data.get("name"),
                    "categories.menu_items.price": float(Decimal(validated_data.get("price"))),
                    "categories.menu_items.food_type": "V" if validated_data.get("veg") else "NV",
                    "categories.menu_items.image_url": validated_data.get("image_url"),
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
            return True
        
        return False
        
    
    
    def item_already_exists(self, validated_data) -> CartItems | None:
        """
        To check if data exists in postgreSQL return it
        """
        try:
            item = CartItems.objects.get(
                cart = validated_data.get("cart").pk,
                name = validated_data.get("name"),
                price = validated_data.get("price"),
                category = validated_data.get("category"),
                veg = validated_data.get('veg'),
                image_url = validated_data.get('image_url'),
            )
            
            return item
        
        except CartItems.DoesNotExist:
            return None
        
        
        
    def create(self, validated_data):
        """
        Before creating check if it even exists in mongodb or not, and if it does then check if its exists in postgresql\n
        and then only create data
        """
        
        is_data_in_mongo: bool = self.data_in_mongoDB(validated_data)
        
        if not is_data_in_mongo:
            raise ValueError("Data Not Found in MongoDB, check for any type or spelling mistake")
        
        
        data_from_postgre: CartItems | None = self.item_already_exists(validated_data)
        
        mode = validated_data.pop("mode", None)
        
        if data_from_postgre and not mode:
            raise ValueError("Data Already exists!! please provide 'mode' key with either 'add' or 'remove' value, to increase or decrease quantity")
                
        
        validated_data.pop('restaurant_id')
        
        if data_from_postgre:
            if mode == "add":
                data_from_postgre.quantity += 1
                data_from_postgre.save()
        
            # TODO: Might delete the data if quantity react to 0 (may be)    
            elif mode == "remove" and data_from_postgre.quantity>0:
                data_from_postgre.quantity -= 1
                data_from_postgre.save()
                
            return data_from_postgre
            

        # Now finally create a new data
        
        return super().create(validated_data)
        


class CartSerializer(serializers.ModelSerializer):
    c_items = CartItemSerializer(many=True)
    
    class Meta:
        model = Cart
        fields = (
            "id",
            "user",
            'total_items',
            'total_price',
            'c_items',
        )
        
        read_only_fields = ("user", "total_items", "total_price")
        
        