from rest_framework import serializers
from restaurants.models import Order, OrderItems

class OrderSerializer(serializers.ModelSerializer):
    restaurant_img = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        exclude = ('user', )
        
    def get_restaurant_img(self, obj: Order):
        order_item = OrderItems.objects.filter(order=obj).first()
        return order_item.image_url