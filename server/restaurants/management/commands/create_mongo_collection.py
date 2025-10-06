from typing import Any
from django.core.management.base import BaseCommand
from restaurants.models import Menu


class Command(BaseCommand):
    help = "Creates mongoDB schema collection mentioned for the first time"
    
    def handle(self, *args: Any, **options: Any) -> str | None:
        
        self.stdout.write("Creating MongoDB schema...")
        
        try:
            Menu.ensure_indexes()
            
            self.stdout.write(
                self.style.SUCCESS(
                    "Successfully created indexes. The 'menus' collection is now ready."
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"An error occurred: {e}")
            )