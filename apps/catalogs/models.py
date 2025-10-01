from django.db.models import (
    Model,
    CharField,
    TextField,
    FloatField,
    BooleanField,
    ForeignKey,
    CASCADE,
    ManyToManyField,
)

from lib.utils import MinValueValidator


class Restaurant(Model):
    """
    Model representing a restaurant.

    Fields:
    - name: The name of the restaurant (CharField, max_length=100).
    - description: A brief description of the restaurant (TextField).
    """

    name = CharField(max_length=100,)
    description = TextField()


class MenuItem(Model):
    """
    Model representing a menu item in a restaurant.

    Fields:
    - restaurant_id: ForeignKey to the Restaurant model (on_delete=CASCADE).
    - name: The name of the menu item (CharField, max_length=100).
    - price: The price of the menu item (FloatField).
    - availability: Availability status of the menu item (BooleanField, default=True).
    """

    restaurant_id = ForeignKey(
        to=Restaurant, 
        on_delete=CASCADE, 
        related_name="menu_items",
    )

    name = CharField(max_length=100,)
    price = FloatField(validators=[MinValueValidator(0.0)],)
    availability = BooleanField(default=True,)


class Category(Model):
    """
    Model representing a category of menu items.

    Fields:
    - name: The name of the category (CharField, max_length=70).
    """

    name = CharField(max_length=70,)


class MenuItemCategory(Model):
    """
    Model representing the many-to-many relationship between MenuItem and Category.

    Fields:
    - menu_item_id: ManyToManyField to the MenuItem model (on_delete=CASCADE).
    - category_id: ManyToManyField to the Category model (on_delete=CASCADE).
    """

    menu_item_id = ManyToManyField(
        to=MenuItem, 
        related_name="categories",
    )
    category_id = ManyToManyField(
        to=Category, 
        related_name="menu_items",
    )


class Option(Model):
    """
    Model representing options for a menu item.

    Fields:
    - menu_item_id: ForeignKey to the MenuItem model (on_delete=CASCADE).
    - name: The name of the option (CharField, max_length=100).
    """

    menu_item_id = ForeignKey(
        to=MenuItem, 
        on_delete=CASCADE, 
        related_name="options",
    )

    name = CharField(max_length=100,)


class ItemOption(Model):
    """
    Model representing the many to many relationship between MenuItem and Options.

    Fields:
    - menu_item_id: ManyToManyField to the MenuItem model (on_delete=CASCADE).
    - option_id: ManyToManyField to the Options model (on_delete=CASCADE).
    - price_delta: The price change associated with the option (FloatField, default=0.0).
    - is_default: Indicates if the option is a default choice (BooleanField, default=False).
    """

    menu_item_id = ManyToManyField(
        to=MenuItem, 
        related_name="item_options",  
    )
    option_id = ManyToManyField(
        to=Option, 
        blank=True,  
        related_name="item_options",
    )
    price_delta = FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0)],                         
    )
    is_default = BooleanField(default=False,)

