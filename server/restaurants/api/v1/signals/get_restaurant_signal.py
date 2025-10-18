from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.core.cache import cache
from restaurants.models import Restaurant


@receiver([post_save, post_delete], sender=Restaurant)
def invalidate_restaurants_cache(sender, instance, *args, **kwargs):
    """
    Removes the restaurant's list cache from redis, when a restaurant data is created, updated or deleted\n
    This signal is registered in `app.py`
    """

    cache.delete_pattern("*restaurants_list*")
