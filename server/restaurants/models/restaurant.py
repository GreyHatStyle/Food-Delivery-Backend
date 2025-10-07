import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models


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
    rating_count_int = models.IntegerField(default=0)

    avg_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    address = models.TextField(blank=True, null=True)
    lic_no = models.CharField(max_length=30, blank=True, null=True)
    r_image_url = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        """
        Will get only number from rating count string, to deal with those "1K+ rating" vs "100+ rating" problem
        """

        count_str: str = self.rating_count_str

        if "K" in count_str:
            count_str = count_str.replace("K", "000")

        rating_count = ""

        for char in count_str:
            if char.isdigit():
                rating_count += char

        self.rating_count_int = int(rating_count) if rating_count != "" else 0
        super().save(*args, **kwargs)

    class Meta:
        db_table = "Restaurants"
