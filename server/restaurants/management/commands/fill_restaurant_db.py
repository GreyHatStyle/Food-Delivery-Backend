import json
import os
from typing import Any

from django.core.management.base import BaseCommand
from django.db import connection
from restaurants.models import Restaurant


class Command(BaseCommand):

    def rating_conversion(self, rating: str) -> float:
        try:
            return float(rating)
        except Exception:
            return 0

    def avg_cost_conversion(self, avg_cost: str) -> float:
        try:
            return float(avg_cost.split(" ")[-1])
        except Exception:
            return 0

    def cuisine_list_conversion(self, cuisine: str) -> list[str]:
        """
        I am writing this particular doc string because my lazy future self
        will surely forgot why I did these many things down below

        1. The string have comma separated cuisine values.
        2. These values certainly not have integrity ["indian", "chinese","italian"]
        (as you can see extra space between comma)
        3. That's why i first `split` it to convert it to list, and then `strip` it to remove leading whitespaces.
        """

        if not cuisine or cuisine.strip() == "":
            return []

        cuisine_list: list[str] = cuisine.split(",")

        return [data.strip() for data in cuisine_list]

    def handle(self, *args: Any, **options: Any) -> str | None:

        path_till_server = os.getcwd()
        json_l_path = os.path.join(
            path_till_server,
            "data",
            "menu-data-1759919994-uuid-digitalOcean.jsonl",
        )

        BULK_INSERT_QUERIES: list[Restaurant] = []

        with open(json_l_path, "r") as fp:

            for line in fp:

                try:
                    restaurant_data = json.loads(line)

                    if "menu" in restaurant_data:
                        del restaurant_data["menu"]

                    rest_query = Restaurant(
                        id=restaurant_data.get("restaurant_uuid"),
                        r_name=restaurant_data.get("name", ""),
                        city=restaurant_data.get("city", ""),
                        cuisine=self.cuisine_list_conversion(
                            restaurant_data.get("cuisine", "")
                        ),
                        rating=self.rating_conversion(restaurant_data.get("rating")),
                        rating_count_str=restaurant_data.get("rating_count"),
                        avg_cost=self.avg_cost_conversion(restaurant_data.get("cost")),
                        address=restaurant_data.get("address"),
                        lic_no=restaurant_data.get("lic_no"),
                    )

                    BULK_INSERT_QUERIES.append(rest_query)

                except Exception as e:
                    print(e)

        Restaurant.objects.bulk_create(objs=BULK_INSERT_QUERIES)

        self.stdout.write(
            self.style.SUCCESS(
                f"Restaurant data created successfully\nConnection Q Len: {len(connection.queries)}"
            )
        )
