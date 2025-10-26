from __future__ import annotations
import uuid
from datetime import date

from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from typing import TYPE_CHECKING


class User(AbstractUser):
    # Reference: https://tomharrisonjr.com/uuid-or-guid-as-primary-keys-be-careful-7b2aa3dcb439

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    phone_no = PhoneNumberField(unique=True)
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="Birthday")

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = [
        "phone_no",
    ]
    
    # Warning: Don't change the variables, before changing the 'related_name' field 
    # in their respective model
    if TYPE_CHECKING:
        from restaurants.models import Order, Cart
        address: models.Manager[UserAddress]
        cart: models.Manager[Cart]
        order: models.Manager[Order]
        
        

    @property
    def age(self):
        today = date.today()
        return relativedelta(today, self.date_of_birth).years

    class Meta:
        db_table = "Users"

    def __str__(self):
        return self.username


class AddressTypeChoices(models.TextChoices):
    HOME = "HOM"
    OFFICE = "OFI"
    OTHER = "OTH"
    

class UserAddress(models.Model):
    # May be analyzers would want to know from which city/state most users are
    # logged in..
    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True, 
        related_name="address"
    )
    
    main_address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    
    # since India can maximum have 6 digit pin code
    pin_code = models.CharField(max_length=6)
    
    address_type = models.CharField(
        max_length=3, 
        choices=AddressTypeChoices,
        default=AddressTypeChoices.HOME,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f"{self.user}'s {self.address_type} Address"
    
    class Meta:
        db_table = "UserAddress"
    