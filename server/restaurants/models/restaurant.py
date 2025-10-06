from django.db import models
from django.contrib.postgres.fields import ArrayField
import uuid

class Restaurant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    r_name = models.CharField(max_length=200)
    city = models.CharField(max_length=20)
    cuisine = ArrayField(
        models.CharField(max_length=20),
        default=list,
        blank=True,
    )
    
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    rating_count_str = models.CharField(max_length=30, blank=True, null=True)
    avg_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    address = models.TextField(blank=True, null=True)
    lic_no = models.CharField(max_length=30, blank=True, null=True)
    r_image_url = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = "Restaurants"
    
    
    
    

