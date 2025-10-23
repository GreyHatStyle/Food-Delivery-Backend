import django_filters
from restaurants.models import Restaurant, Menu
from logging import getLogger
from utils import print_red, print_green
from pprint import pprint

logger = getLogger("restaurants")

class GetAllRestaurantsFilter(django_filters.FilterSet):
    cuisine = django_filters.CharFilter(method="filter_by_cuisine")
    search = django_filters.CharFilter(method="filter_by_food_name_search", label="search")
    

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
    
    def filter_by_food_name_search(self, queryset, name, value: str):
        """
        Find the restaurants with food name, like if user asks "search=burg", then returns all restaurants that have "Burger"\n
        - value: burg
        
        """
        
        if not value:
            return queryset
        
        try:
            
            """
            Its IMPORTANT OPTIMIZATION, so I think I should write about this:
            
            PROBLEM:
            - Without letting django do its filtering first, the code was applying filter on mongoDB first, and then after receiving the "restaurant_id"s, the filters (for postgresql) were applying in queryset.
            - Because of which, mongoDB was basically searching all 1,00,000 records first for value "burg", and then returning the "restaurant_id"s of matching query.
            - These "restaurant_id"s were then used to filter (around with other filters) on 5000 restaurant's data in PostgreSQL.
            - This was taking around 530ms to 800ms (locally) per request.
            
            
            SOLUTION:
            When I figured it out (by printing it), I realized it should be opposite:
            
            1. Filters should be applied on "restaurants" table (in postgresql), which are only around 5000, and return their "restaurant_id"s.
            2. Then MongoDB should use those "restaurant_id"s to perform search for food value "burg" to get Burgers. on limited ids.
            3. This will save MongoDB to search only of required filtered records, instead of speed running on 1 Lakh records first.
            
            Believe it or not, this approach now takes only around 88ms to 120ms (locally) per request. 
            
            Yes, around 5x performance increase!!!
            
            """
            
            
            
            # This is the code, that let django perform filter first on PostgreSQL, and then return the required "restaurant_id"s
            filtered_restaurants_ids = list(queryset.values_list('id', flat=True))
            
            if not filtered_restaurants_ids:
                return queryset.none()
            
            filtered_str_uuids = [
                str(id) for id in filtered_restaurants_ids
            ]
            
            # print_green("==============================================================================================================")
            # pprint(filtered_str_uuids)
            # print_green("==============================================================================================================")
            
            
            # After that mongoDB code :)
            pipeline = [
                {
                  "$match": {
                      "restaurant_id": {
                          "$in": filtered_str_uuids,
                      }
                  }  
                },
                {"$unwind": "$categories"},
                {"$unwind": "$categories.menu_items"},
                {
                    "$match": {
                        "categories.menu_items.name":{
                            "$regex": value,
                            "$options": "i",
                        }
                    }
                },
                 {
                    "$group": {
                        "_id": "$restaurant_id"
                    }
                },
            ]
            
            agg = Menu.objects.aggregate(pipeline)
            results = list(agg)
            # print_green("==============================================================================================================")
            # pprint(results)
            # print_green("==============================================================================================================")
            
            # To get only unique rest_id, since aggregation pipeline can return multiple rest_ids
            results_rest_id = [
                r.get("_id") for r in results if r.get("_id")
            ]
            
            
            if not results_rest_id:
                return queryset.none()
            
            return queryset.filter(id__in=results_rest_id)
        
        except Exception as e:
            logger.error(f"Search Mongo error: {e}")
            print_red(f"Search Mongo error: {e}")
            return queryset
            
