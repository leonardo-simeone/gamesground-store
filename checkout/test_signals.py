from django.test import TestCase
from django.contrib.auth.models import User
from .models import Order, OrderLineGame
from games.models import *


class TestSignals(TestCase):

    """
    The setUp method is used to create User, Pegi, Platform, Game,
    Order and OrderLineGame objects.
    - test_update_on_save: Tests that on game line quantity update
    the order total is updated accordingly.
    - test_update_on_delete: Tests that when the line games are deleted
    the order total is set to zero.
    """

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
            )

        # Create pegi and platform
        self.pegi = Pegi.objects.create(age=18)
        self.platform = Platform.objects.create(name='Test Platform')
        # Create a test game
        self.game = Game.objects.create(
            name='Test Game',
            genre=['Action'],
            description='This is a test game.',
            year='2023',
            platform=self.platform,
            price=25.00,
            pegi_rating=self.pegi,
            image=None,
            available_in_other_consoles=False,
            trailer='https://www.youtube.com/watch?v=video-id'
        )

        # Create a test order
        self.order = Order.objects.create(
            order_number='56E3AC1F12814832AB8397205867DCB4',
            full_name='Test User',
            email='test@example.com',
            phone_number='1234567890',
            country='US',
            town_or_city='Test City',
            street_address1='123 Test St',
        )

        # Create a test order line game
        self.order_line_game = OrderLineGame.objects.create(
            order=self.order,
            game=self.game,
            quantity=1,
            linegame_total=25.00,
        )

    def test_update_on_save(self):
        # Update the OrderLineGame
        self.order_line_game.quantity = 2
        self.order_line_game.save()

        # Check if the order's total has been updated
        self.order.refresh_from_db()
        self.assertEqual(self.order.order_total, 50.00)
        self.assertEqual(self.order.grand_total, 50.00)

    def test_update_on_delete(self):
        # Delete the OrderLineGame
        self.order_line_game.delete()

        # Check if the order's total has been updated
        self.order.refresh_from_db()
        self.assertEqual(self.order.order_total, 0.00)
        self.assertEqual(self.order.grand_total, 0.00)
