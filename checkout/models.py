import uuid

from django.db import models
from django.db.models import Sum
from django.conf import settings

from django_countries.fields import CountryField


from games.models import Game
from profiles.models import UserProfile


class Order(models.Model):
    """
    A model to create an order table in the database
    and create order objects. There is one particular
    relationship in the model, the user profile field has
    a FK relationship with UserProfile model. It has four
    helper methods, one to create the order number, one to update
    the order total, one to save the order number and one to
    represent the objects with the order number.
    """

    order_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='orders'
        )
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0
        )
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
        )
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
        )

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total each time a line game is added,
        accounting for delivery costs.
        """
        self.order_total = self.linegames.aggregate(
            Sum('linegame_total'))['linegame_total__sum'] or 0
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            if self.order_total == 0:
                self.delivery_cost = 0
            else:
                self.delivery_cost = settings.STANDARD_DELIVERY_CHARGE
        else:
            self.delivery_cost = 0
        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineGame(models.Model):
    """
    A model to create an order line game table in the database
    and create order line game objects. There are two particular
    relationships in the model, the order field has
    a FK relationship with order model and the game field
    has a FK relationship with game model. It has two
    helper methods, one to calculate line game total and one
    to represent the objects with a custom string
    """

    order = models.ForeignKey(
        Order,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='linegames'
        )
    game = models.ForeignKey(
        Game, null=False, blank=False, on_delete=models.CASCADE
        )
    quantity = models.IntegerField(null=False, blank=False, default=0)
    linegame_total = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=False,
        blank=False,
        editable=False)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the linegame total
        and update the order total.
        """
        self.linegame_total = self.game.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f'{self.game.name}, id number: '
            f'{self.game.id} on order {self.order.order_number}'
        )
