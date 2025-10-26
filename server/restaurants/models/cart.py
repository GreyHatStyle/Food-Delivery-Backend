from __future__ import annotations
from django.db import models
from account.models import User
from typing import TYPE_CHECKING
from django.db.models import Manager


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f"{self.user.username}'s cart"
    
    if TYPE_CHECKING:
        # Adding this Manager type to tell linter to trust me, instead of throwing errors
        c_items: Manager[CartItems]
    
    @property
    def total_quantity(self):
        result = self.c_items.aggregate(total_quantity=models.Sum("quantity"))
        return result["total_quantity"] or 0
    
    @property
    def total_items(self):
        return self.c_items.count()
    
    @property
    def total_price(self):
        result = self.c_items.aggregate(
            total_price=models.Sum("price"),
        )
        return result["total_price"] or 0
    
    class Meta:
        db_table = "Cart"


# TODO: setup a signal to delete this item, if item is deleted from 'MenuItems' in mongoDB
class CartItems(models.Model):
    cart = models.ForeignKey(
        Cart, 
        on_delete=models.CASCADE, 
        related_name='c_items',
        db_index=True,    
    )
    
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image_url = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=50)
    quantity = models.IntegerField(default=1)
    veg = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f"{self.quantity} x {self.name} in {self.cart.user.username}'s cart"
    
    class Meta:
        db_table = "CartItems"
