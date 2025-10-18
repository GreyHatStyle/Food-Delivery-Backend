import django_filters
from restaurants.models import Restaurant


class GetAllRestaurantsFilter(django_filters.FilterSet):
    cuisine = django_filters.CharFilter(method="filter_by_cuisine")

    class Meta:
        model = Restaurant
        fields = {
            "city": ["iexact"],
            "rating": ["gte"],
            "avg_cost": ["lte", "gte", "range"],
            "rating_count_int": ["gte"],
        }

    def filter_by_cuisine(self, queryset, name, value: str):
        """
        Should filter the array type query passed in params like `?cuisine=american,pizza`
        """
        cuisines = [c.strip() for c in value.split(",")]

        return queryset.filter(cuisine__contains=cuisines)
