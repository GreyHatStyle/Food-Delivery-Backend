import uuid
from datetime import date

from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


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

    @property
    def age(self):
        today = date.today()
        return relativedelta(today, self.date_of_birth).years

    class Meta:
        db_table = "Users"

    def __str__(self):
        return self.username
