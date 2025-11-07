from __future__ import annotations
from django.db import models
from account.models import User
from typing import TYPE_CHECKING
from django.db.models import Manager


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    restaurant = models.ForeignKey("restaurants.Restaurant", on_delete=models.CASCADE, related_name='carts')
    
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
    
    class Meta:
        db_table = "Cart"



class CartItems(models.Model):
    """
    With time I felt, if a restaurant decided to increase the rate of an item or remove it, while the person had that item in cart with previous cheaper rate, it may cause conflicts while ordering, hence storing only 'item_uuid' in cart is safer.
    """
    cart = models.ForeignKey(
        Cart, 
        on_delete=models.CASCADE, 
        related_name='c_items',
        db_index=True,    
    )
    
    item_uuid = models.CharField(max_length=40)
    category = models.CharField(max_length=50)
    quantity = models.IntegerField(default=1)
    
    def __str__(self) -> str:
        return f"{self.quantity} x {self.item_uuid} in {self.cart.user.username}'s cart"
    
    class Meta:
        db_table = "CartItems"
