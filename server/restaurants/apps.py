from django.apps import AppConfig


class RestaurantsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "restaurants"

    def ready(self) -> None:
        """
        To register the signals
        """
        from .api.v1 import signals

        return super().ready()
