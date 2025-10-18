from ..serializers import RestaurantSerializer
from rest_framework.serializers import SerializerMethodField
from restaurants.models import Menu, Restaurant
from utils import SysPrint


class MenuSerializer(RestaurantSerializer):

    menu_data = SerializerMethodField()
    category = SerializerMethodField()

    sys_p = SysPrint()

    def __init__(self, *args, **kwargs):
        self.category = kwargs.pop("category", None)
        super().__init__(*args, **kwargs)

    
    
    class Meta(RestaurantSerializer.Meta):

        fields = RestaurantSerializer.Meta.fields + [
            "address",
            "category",
            "menu_data",
        ]

    
    def category_pipeline(self, restaurant: Restaurant) -> dict:
        """
        Pipeline for returning category names => category: { names: ["cat1", "cat2", ...]}
        """
        try:
            categories_pipeline = Menu.objects.aggregate(
                [
                    {
                        "$match": {
                            "restaurant_id": str(restaurant.id),
                        }
                    },
                    {
                        "$project": {
                            # "categories": 1,
                            "_id": 0,
                            "names": "$categories.name",
                        }
                    },
                ]
            )

            return categories_pipeline

        except Exception as e:
            self.sys_p.print_error(f"Error: {e}")
            return {}

    def get_category(self, restaurant: Restaurant):
        return self.category_pipeline(restaurant)

    def get_menu_data(self, restaurant: Restaurant):
        """
        Gets, selected self.category menu data only, if self.category not given then finds first category from
        pipe line and returns it's menu items instead
        """

        category_to_find = ""

        if self.category:
            category_to_find = str(self.category)

        else:
            category = list(self.category_pipeline(restaurant))
            print("Category: ", category)
            if category:
                category_to_find = category[0]["names"][0]

        try:
            menu_items = Menu.objects.aggregate(
                [
                    {
                        "$match": {
                            "restaurant_id": str(restaurant.id),
                        }
                    },
                    # So here, when I $unwind the categories, it divided it into json sets(as it says),
                    # and then I can use $match to select particular set and display it using $project
                    # cool huh?? No python latency, everything processing handled by mongoDB only.
                    {
                        "$unwind": "$categories",
                    },
                    {
                        "$match": {
                            "categories.name": category_to_find,
                        }
                    },
                    # This last step is important to automatically serialize the filtered data from pipeline
                    # and display it.
                    {
                        "$project": {
                            "_id": 0,
                        }
                    },
                ]
            )

            return menu_items

        except Exception as e:
            self.sys_p.print_error(f"Exception: {e}")
