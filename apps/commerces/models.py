from django.db.models import (
    Model,
    IntegerField,
    CharField,
    DateTimeField,
    ForeignKey,
    CASCADE,
    PROTECT,
    FloatField,
    BooleanField,
    ManyToManyField,
)

from apps.catalogs.models import MenuItem, Option

from lib.utils import MinValueValidator, MaxValueValidator


class User(Model):
    """
    Model representing a user in the system.

    Fields:
    - nickname: The nickname of the user (CharField, max_length=100).
    """

    nickname = CharField(max_length=100)


class Address(Model):
    """
    Model representing an address.

    Fields:
    - user_id: ForeignKey to the User model (on_delete=CASCADE).
    """

    user_id = ForeignKey(
      to=User, 
      on_delete=CASCADE, 
      related_name="addresses",
    )


class Order(Model):
    """
    Model representing an order.

    Fields:
    - user_id: ForeignKey to the User model (on_delete=PROTECT).
    - address_id: ForeignKey to the Address model (on_delete=PROTECT).
    - status: The status of the order (IntegerField, choices).
    - total_price: The total price of the order (FloatField).
    - created_at: The timestamp when the order was created (DateTimeField, auto_now_add=True).
    - updated_at: The timestamp when the order was last updated (DateTimeField, auto_now=True).
    """

    STATUS_CHOICES = (
        (0, "New"),
        (1, "Confirmed"),
        (2, "Delivering"),
        (3, "Done"),
    )

    user_id = ForeignKey(
        to=User,
        on_delete=PROTECT,
        related_name="orders",
    )
    address_id = ForeignKey(
        to=Address, 
        on_delete=PROTECT, 
        related_name="orders",
    )
    status = IntegerField(default=0,)
    total_price = FloatField(validators=[MinValueValidator(0.0)],)
    subTotal_price = FloatField(validators=[MinValueValidator(0.0)],)
    discount_total = FloatField(
        default=0.0, 
        validators=[
            MinValueValidator(0.0), 
            MaxValueValidator(100.0)
        ],
    )
    created_at = DateTimeField(auto_now_add=True,)
    updated_at = DateTimeField(auto_now=True,)


class OrderItem(Model):
    """
    Model representing an item in an order.

    Filed:
    - order_id: ForeignKey to the Order model (on_delete=CASCADE).
    - menu_item_name: The name of the menu item (CharField, max_length=100).
    - menu_item_price: The price of the menu item (FloatField).
    - quantity: The quantity of the menu item ordered (IntegerField, gte=1).
    - line_total: The total price for this line item (FloatField).
    """    

    order_id = ForeignKey(
        to=MenuItem,
        on_delete=CASCADE,
        related_name="order_items",
    )
    menu_item_name = CharField(max_length=100,)
    menu_item_price = FloatField(
        validators=[MinValueValidator(0.0)],
    )
    quantity = IntegerField(
        validators=[MinValueValidator(1)],
    )
    line_total = FloatField(
        validators=[MinValueValidator(0.0)],
    )


class OrderItemOption(Model):
    """"""

    order_item_id = ForeignKey(
        to=OrderItem,
        on_delete=CASCADE,
        related_name="item_options",
    )
    option_id = ForeignKey(
        to=Option,
        on_delete=CASCADE,
        related_name="order_item_options",
    )


class Promo(Model):
    """
    Model representing a promotional code.

    Fields:
    - name: The name of the promo code (CharField, max_length=20).
    - description: A brief description of the promo code (CharField, max_length=100).
    - discount: The discount percentage (IntegerField, gte=0, lte=100).
    - is_active: Indicates if the promo code is active (BooleanField, default=True).
    """

    name = CharField(max_length=20,)
    description = CharField(max_length=100,)
    discount = IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    is_active = BooleanField(default=True,)


class OrderPromo(Model):
    """"""

    order_id = ManyToManyField(
        to=Order,
        related_name="order_promos",
    )
    promo_id = ManyToManyField(
        to=Promo,
        related_name="order_promos",
    )

