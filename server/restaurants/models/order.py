from __future__ import annotations
from django.db import models
from typing import TYPE_CHECKING
from account.models import User

class OrderStatusChoices(models.TextChoices):
    CANCELLED = "CAN"
    DELIVERED = "DEL"
    PENDING = "PEN"
    
class PaymentTypeChoices(models.TextChoices):
    UPI = "UPI"
    CARD = "CAR"
    CASH_ON_DELIVERY = "COD"



class Order(models.Model):
    # Setting it to null because this order info might be used by analyzers 
    # to study *which products are ordered together frequently with each other*
    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True, 
        related_name="order"
    )
    restaurant = models.ForeignKey(
        "restaurants.Restaurant", 
        on_delete=models.SET_NULL, 
        related_name='orders',
        null=True,
        blank=True,    
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=3, 
        choices=OrderStatusChoices, 
        default=OrderStatusChoices.PENDING,
    )
    
    # making address text field instead of relation, because User's address can change with time
    delivery_address = models.TextField()
    payment_type = models.CharField(
        max_length=3, 
        choices=PaymentTypeChoices,
        default=PaymentTypeChoices.CASH_ON_DELIVERY,
    )
    card_name = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self) -> str:
        return f"{self.user.username}'s Order"
    
    if TYPE_CHECKING:
        o_items: models.Manager[OrderItems]
        
        
    @property
    def total_items(self):
        return self.o_items.count()
    
    @property
    def total_price(self):
        result = self.o_items.aggregate(
            total_price = models.Sum("price"),
        )
        return result["total_price"] or 0
    
    class Meta:
        db_table = "Order"
    

class OrderItems(models.Model):
    order = models.ForeignKey(
        Order, 
        on_delete=models.SET_NULL, 
        null=True,
        blank=True,
        related_name='o_items', 
        db_index=True
    )
    
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image_url = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=50)
    quantity = models.IntegerField(default=1)
    veg = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f"{self.quantity} x {self.name} in {self.order.user.username}'s cart"

    class Meta:
        db_table = "OrderItems"

    
    