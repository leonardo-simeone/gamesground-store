import uuid
from decimal import Decimal
from django.test import TestCase
from django.conf import settings
from django_countries.fields import Country
from django.contrib.auth.models import User
from django.conf import settings

from games.models import Game
from profiles.models import UserProfile
from .models import *


class TestOrderModel(TestCase):

    """
    The setUp method is used to create User, Game, Order and
    OrderLineGame objects.
    We have several test methods covering different
    aspects of the Order model.
    - test_generate_order_number: Tests that the order number
    and the order generated correctly.
    - test_update_total_standard_delivery: Tests when a game is added and
    update total matches (or surpasses) the free delivery threshold,
    delivery cost equals zero.
    - test_update_total_zero_total: Tests that total equals zero once all line
    games are deleted.
    - test_save_generate_order_number: Tests that order number and order
    are correctly saved.
    - test_str_representation: Tests order string output is correct.
    """

    def setUp(self):
        # Create a sample user
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword"
        )

        # Create a sample game
        self.game = Game.objects.create(
            name='Test Game',
            description='This is a test game.',
            year='2023', price=10.00,
            available_in_other_consoles=False,
            trailer='https://www.youtube.com/watch?v=video-id'
        )

        # Create a sample order
        self.order = Order.objects.create(
            user_profile=UserProfile.objects.get(user=self.user),
            full_name='Test User',
            email='test@example.com',
            phone_number='1234567890',
            country=Country(code='US'),
            postcode='12345',
            town_or_city='Test City',
            street_address1='123 Test St',
            delivery_cost=7.00,
            order_total=20.00,
            grand_total=27.00,
        )
        self.order.linegames.create(
            game=self.game, quantity=2, linegame_total=Decimal('20.00')
            )

    # Test generate order number
    def test_generate_order_number(self):
        order = Order.objects.create(
            user_profile=UserProfile.objects.get(user=self.user),
            full_name='Test User 2',
            email='test2@example.com',
            phone_number='9876543210',
            country=Country(code='CA'),
            postcode='V6B 2E2',
            town_or_city='Vancouver',
            street_address1='456 Test Ave',
        )
        self.assertIsNotNone(order.order_number)
        self.assertEqual(len(order.order_number), 32)

    # Test add one more line game and update total
    def test_update_total_standard_delivery(self):
        self.order.linegames.create(
            game=self.game, quantity=1, linegame_total=Decimal('10.00')
            )
        self.order.update_total()
        expected_total = Decimal('30.00')
        expected_grand_total = Decimal('30.00')
        self.assertEqual(self.order.order_total, expected_total)
        self.assertEqual(self.order.grand_total, expected_grand_total)
        self.assertEqual(self.order.delivery_cost, 0)

    # Test totals when remove all line games
    def test_update_total_zero_total(self):
        self.order.linegames.all().delete()
        self.order.update_total()
        self.assertEqual(self.order.order_total, 0)
        self.assertEqual(self.order.grand_total, 0)

    # Test order number and order are correctly saved
    def test_save_generate_order_number(self):
        order = Order(
            user_profile=UserProfile.objects.get(user=self.user),
            full_name='Test User 3',
            email='test3@example.com',
            phone_number='5555555555',
            country=Country(code='GB'),
            postcode='SW1A 1AA',
            town_or_city='London',
            street_address1='10 Downing Street',
        )
        order.save()
        self.assertIsNotNone(order.order_number)
        self.assertEqual(len(order.order_number), 32)

    # Test order string output is correct
    def test_str_representation(self):
        self.assertEqual(str(self.order), self.order.order_number)


class TestOrderLineGameModel(TestCase):

    """
    The setUp method is used to create User, Game, Order and
    OrderLineGame objects.
    We have several test methods covering different
    aspects of the Order line game model.
    - test_save_linegame_total: Tests when we add two line games the
    total for the line game object is saved correctly.
    - test_update_order_total_on_save: Tests that when a line game is added,
    the order total is updated accordingly.
    - test_str_representation: Tests order line game string output is correct.
    """

    def setUp(self):
        # Create a sample user
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword"
        )

        # Create a sample game
        self.game = Game.objects.create(
            name='Test Game',
            description='This is a test game.',
            year='2023', price=Decimal('25.00'),
            available_in_other_consoles=False,
            trailer='https://www.youtube.com/watch?v=video-id'
        )

        # Create a sample order
        self.order = Order.objects.create(
            user_profile=UserProfile.objects.get(user=self.user),
            full_name='Test User',
            email='test@example.com',
            phone_number='1234567890',
            country=Country(code='US'),
            postcode='12345',
            town_or_city='Test City',
            street_address1='123 Test St',
            delivery_cost=0,
            order_total=100,
            grand_total=100,
        )
        self.order.linegames.create(
            game=self.game, quantity=4, linegame_total=Decimal('100.00')
            )

    # Test line game total is updated correctly
    def test_save_linegame_total(self):
        linegame = OrderLineGame.objects.create(
            order=self.order,
            game=self.game,
            quantity=2,
        )
        expected_total = Decimal('50.00')
        self.assertEqual(linegame.linegame_total, expected_total)

    # Test order total is updated correctly
    def test_update_order_total_on_save(self):
        # Initially, the order total is 100
        self.assertEqual(self.order.order_total, Decimal('100.00'))

        linegame = OrderLineGame.objects.create(
            order=self.order,
            game=self.game,
            quantity=3,
        )

        self.order.update_total()

        # Now, after adding the linegame, the order total should be updated
        expected_order_total = Decimal('175.00')
        self.assertEqual(self.order.order_total, expected_order_total)

    # Test order line game string output is correct
    def test_str_representation(self):
        linegame = OrderLineGame.objects.create(
            order=self.order,
            game=self.game,
            quantity=1,
        )
        expected_str = (
            f'{self.game.name}, id number: {self.game.id} on order '
            f'{self.order.order_number}'
            )
        self.assertEqual(str(linegame), expected_str)
