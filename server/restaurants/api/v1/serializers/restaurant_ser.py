import logging

from rest_framework import serializers
from restaurants.models import Menu, Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    logger = logging.getLogger("restaurants")

    menu_image = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = [
            "id",
            "r_name",
            "rating",
            "avg_cost",
            "rating_count_str",
            "cuisine",
            "menu_image",
            "r_image_url",
        ]

    def get_menu_image(self, restaurant: Restaurant):
        """
        Get the Image url of first menu item found, that has image.\n
        This field will be used as fallback if restaurant owner hasn't uploaded their restaurant image.
        """

        try:
            pipe_line = Menu.objects.aggregate(
                [
                    {
                        "$match": {"restaurant_id": str(restaurant.id)},
                    },
                    {"$unwind": "$categories"},
                    {"$unwind": "$categories.menu_items"},
                    {
                        "$match": {
                            "categories.menu_items.image_url": {
                                "$exists": True,
                                "$ne": "no_url_image",
                            },
                        }
                    },
                    {"$limit": 1},
                    {
                        "$project": {
                            "image_url": "$categories.menu_items.image_url",
                            "_id": 0,
                        }
                    },
                ]
            )

            result_list = list(pipe_line)

            if result_list and "image_url" in result_list[0]:

                # BUG:For some reason this logger is not working for files,
                # but same configuration is working in "accounts" views, Deal with it if possible
                self.logger.debug(result_list)

                return result_list[0]["image_url"]

            return ""

        except Exception as e:
            print(e)

            return ""
        
        
    
