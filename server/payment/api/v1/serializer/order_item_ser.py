from rest_framework import serializers
from restaurants.models import OrderItems

class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        exclude = ('id', 'order', 'category')