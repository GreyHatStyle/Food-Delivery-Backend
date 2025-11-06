from mongoengine import (
    DecimalField,
    Document,
    EmbeddedDocument,
    EmbeddedDocumentField,
    ListField,
    QuerySet,
    StringField,
    URLField,
)
from uuid import uuid4

FOOD_TYPE_CHOICES = (("V", "Veg"), ("NV", "Non-Veg"), ("E", "Contains Egg"))


class MenuItem(EmbeddedDocument):
    """
    Represent a single Item in menu, like: Butter Paneer masala
    """
    item_uuid = StringField(default=uuid4())
    name = StringField(required=True)
    price = DecimalField(precision=2, required=True)
    food_type = StringField(required=True, choices=FOOD_TYPE_CHOICES)

    image_url = URLField()


class MenuCategory(EmbeddedDocument):
    """
    Recommended menu items, or category like indian, chinese etc.
    """

    name = StringField(required=True)
    menu_items = ListField(EmbeddedDocumentField(MenuItem))


class Menu(Document):
    """
    The final menu collection
    """

    # TODO: for some reason UUID field was not working... so providing string field for now (to store UUID4)
    restaurant_id = StringField(required=True, unique=True)
    categories = ListField(EmbeddedDocumentField(MenuCategory))

    meta = {
        "collection": "menus",
        "indexes": [
            {
                "fields": ["restaurant_id"],
                "unique": True,
            }
        ],
    }

    objects: QuerySet
