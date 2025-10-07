from django.core.management.base import BaseCommand
from restaurants.models import Restaurant


class Command(BaseCommand):
    help = "Made this just to fill new rating_count_num value don't use it otherwise"

    def handle(self, *args, **options):
        """
        rating_count_str wasn't good for ordering, and it was not accepting serializer method field, so..
        Made this command only to fill the new rating, for sql ordering.
        """
        for restaurant in Restaurant.objects.all():

            restaurant.save()

        self.stdout.write(self.style.SUCCESS("Rating count field populated"))
