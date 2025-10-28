from rest_framework import serializers
from restaurants.models import Cart, CartItems

class CartItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = CartItems
        fields = [
            'id',
            'name',
            'price',
            'image_url',
            'category',
            'quantity',
            'veg',
            'cart',
        ]
        


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
        
        
    def create(self, validated_data):
        items_data = validated_data.pop('c_items', [])
        
        cart = Cart.objects.create(**validated_data)
        
        for item in items_data:
            CartItems.objects.create(cart=cart, **item)
            
        return cart
    
    # TODO: Update has stopped working since I allowed cart id, please do something about this shit
    def update(self, instance: Cart, validated_data):
        items_data = validated_data.pop('c_items', [])
        
        instance.c_items.all().delete()
        
        for item in items_data:
            CartItems.objects.create(cart=instance, **item)
            
        instance.save()
        
        return instance
        