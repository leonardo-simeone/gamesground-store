import unittest
from decimal import Decimal
from django.conf import settings
from django.test import RequestFactory, TestCase
from django.contrib.sessions.middleware import SessionMiddleware
from games.models import Game
from .contexts import basket_contents


class TestBasketContents(TestCase):

    """
    The setUp method is used to create a game object and to
    setup a session request.
    We have two test methods: test_basket_contents_empty and
    test_basket_contents_with_items.
    - test_basket_contents_empty: Tests the basket contents when the basket
    is empty.
    - test_basket_contents_with_items: Tests the basket contents when games
    are added to the basket and assertEqual that the games are actually added
    and that the variables are correct.
    """

    def setUp(self):
        # Create a game
        self.game = Game.objects.create(
            name='Test Game', description='This is a test game.',
            year='2023', price=Decimal('29.99'),
            available_in_other_consoles=False,
            trailer='https://www.youtube.com/watch?v=video-id'
            )

        # Set up a request
        self.factory = RequestFactory()
        self.request = self.factory.get('/basket/')
        self.request.session = {}
        middleware = SessionMiddleware()
        middleware.process_request(self.request)

    def test_basket_contents_empty(self):
        # Test basket contents with an empty basket
        context = basket_contents(self.request)

        self.assertEqual(context['basket_items'], [])
        self.assertEqual(context['total'], 0)
        self.assertEqual(context['game_count'], 0)
        self.assertEqual(
            context['delivery'],
            Decimal(settings.STANDARD_DELIVERY_CHARGE)
            )
        self.assertEqual(
            context['free_delivery_delta'],
            settings.FREE_DELIVERY_THRESHOLD
            )
        self.assertEqual(
            context['free_delivery_threshold'],
            settings.FREE_DELIVERY_THRESHOLD
            )
        self.assertEqual(
            context['grand_total'],
            Decimal(settings.STANDARD_DELIVERY_CHARGE))

    def test_basket_contents_with_items(self):
        # Add games to the basket
        self.request.session['basket'] = {str(self.game.pk): 2}

        context = basket_contents(self.request)

        self.assertEqual(len(context['basket_items']), 1)
        self.assertEqual(context['total'], self.game.price * 2)
        self.assertEqual(context['game_count'], 2)
        self.assertEqual(context['delivery'], 0)
        self.assertEqual(context['free_delivery_delta'], 0)
        self.assertEqual(
            context['free_delivery_threshold'],
            settings.FREE_DELIVERY_THRESHOLD
            )
        self.assertEqual(
            context['grand_total'],
            self.game.price * 2 + context['delivery']
            )
