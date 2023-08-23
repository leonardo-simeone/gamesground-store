import unittest
from django.test import RequestFactory, TestCase, Client
from django.shortcuts import reverse, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import get_messages
from decimal import Decimal
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware
from .views import *
from games.models import *


class TestBasketSummaryView(TestCase):

    """
    The setUp method is used to setup a session request.
    - test_basket_summary_view: Tests that the basket request
    is successful and that the basket template content is correct.
    """

    def setUp(self):
        # Set up a request
        self.factory = RequestFactory()
        self.request = self.factory.get(reverse('basket_summary'))
        self.request.session = {}
        middleware = SessionMiddleware()
        middleware.process_request(self.request)

    def test_basket_summary_view(self):
        response = basket_summary(self.request)

        self.assertEqual(response.status_code, 200)

        # Check if the rendered content contains specific
        # template tags and strings
        self.assertContains(response, '<h2 class="mb-4">Shopping Basket</h2>')


class TestAddToBasketView(TestCase):

    """
    The setUp method is used to create Game, User and Platform objects,
    set up a client and messages.
    We have several test methods covering different
    aspects of the add to basket view.
    - In test_add_to_basket_view, we login a user, add a game to the basket
    and check that the game was added correctly and that the message generated
    is correct.
    - test_add_to_basket_with_existing_game, we login a user, add one game
    to the basket and verify that it was added and that the response code is
    correct then add two more games and verify that the quantity was updated
    successfully.
    - test_add_to_basket_view_with_platform, we test that when a game that has
    a platform atrtribute is added to the basket the correct messages is
    generated.
    - In test_add_to_basket_redirect, we simply add a game to the basket and
    verify that the redirect is correct.
    """

    def setUp(self):
        # Create a platform
        self.platform = Platform.objects.create(name='Test Platform')
        # Create a game
        self.game = Game.objects.create(
            name='Test Game', description='This is a test game.',
            year='2023', price=Decimal('29.99'),
            available_in_other_consoles=False,
            trailer='https://www.youtube.com/watch?v=video-id'
            )
        # Create a second game with platform
        self.game2 = Game.objects.create(
            name='Test Game', description='This is a test game.',
            year='2023', price=Decimal('29.99'),
            platform=self.platform,
            available_in_other_consoles=False,
            trailer='https://www.youtube.com/watch?v=video-id'
            )

        # Create a user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
            )

        # Set up a client
        self.client = Client()

        # Manually add the messages middleware
        self.messages_middleware = MessageMiddleware()

    def test_add_to_basket_view(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('add_to_basket', args=[self.game.pk]),
            {'quantity': 2, 'redirect_url': '/'}
            )

        self.assertEqual(response.status_code, 302)

        # Check if the game was added to the basket correctly
        basket = self.client.session.get('basket', {})
        self.assertIn(str(self.game.pk), basket)
        self.assertEqual(basket[str(self.game.pk)], 2)

        # Check if the success message is in the messages
        messages_list = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(
            messages_list[0].message,
            f'Added {self.game.name} to your basket'
            )

    def test_add_to_basket_with_existing_game(self):
        # Add the game to the basket first
        self.client.force_login(self.user)
        self.client.session['basket'] = {str(self.game.pk): 1}
        response = self.client.post(
            reverse('add_to_basket', args=[self.game.pk]),
            {'quantity': 1, 'redirect_url': '/'}
            )
        basket = self.client.session.get('basket', {})
        self.assertEqual(basket[str(self.game.pk)], 1)

        response = self.client.post(
            reverse('add_to_basket', args=[self.game.pk]),
            {'quantity': 2, 'redirect_url': '/'}
            )

        self.assertEqual(response.status_code, 302)

        # Check if the quantity of the existing game in the basket was updated
        basket = self.client.session.get('basket', {})
        self.assertEqual(basket[str(self.game.pk)], 3)

    def test_add_to_basket_view_with_platform(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('add_to_basket', args=[self.game2.pk]),
            {'quantity': 2, 'redirect_url': '/'}
        )

        self.assertEqual(response.status_code, 302)

        basket = self.client.session.get('basket', {})
        self.assertIn(str(self.game2.pk), basket)
        self.assertEqual(basket[str(self.game2.pk)], 2)

        messages_list = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(
            messages_list[0].message,
            f'Added {self.game2.name} {self.game2.platform} to your basket'
        )

    def test_add_to_basket_redirect(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('add_to_basket', args=[self.game.pk]),
            {'quantity': 2, 'redirect_url': '/'}
            )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')


class TestAdjustBasketView(TestCase):

    """
    The setUp method is used to create Game, User and Platform objects,
    set up a client and messages.
    We have several test methods covering different
    aspects of the adjust basket view.
    - In test_adjust_basket_view_quantity_greater_than_zero,
    we login a user, add a game to the basket, adjust the game quantity
    to three in the basket and check that the game quantity was
    updated correctly and that the message generated is correct.
    - In test_adjust_basket_view_with_platform_quantity_greater_than_zero,
    we test that when the basket content is adjusted with a game that
    has platform attribute, the message generated is correct.
    - In test_adjust_basket_view_quantity_zero, we login a user,
    add a game to the basket, adjust the game quantity to zero
    in the basket and check that the game was removed correctly
    and that the message generated is correct.
    - In test_adjust_basket_view_with_platform_quantity_zero, we test
    the same as in the previous method but this time with a game that
    has platform attribute to check the correct message is generated
    """

    def setUp(self):
        # Create a platform
        self.platform = Platform.objects.create(name='Test Platform')
        # Create a game
        self.game = Game.objects.create(
            name='Test Game', description='This is a test game.',
            year='2023', price=Decimal('29.99'),
            available_in_other_consoles=False,
            trailer='https://www.youtube.com/watch?v=video-id'
            )
        # Create a second game with platform
        self.game2 = Game.objects.create(
            name='Test Game', description='This is a test game.',
            year='2023', price=Decimal('29.99'),
            platform=self.platform,
            available_in_other_consoles=False,
            trailer='https://www.youtube.com/watch?v=video-id'
            )

        # Create a user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
            )

        # Set up a client
        self.client = Client()

        # Manually add the messages middleware
        self.messages_middleware = MessageMiddleware()

    def test_adjust_basket_view_quantity_greater_than_zero(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('add_to_basket', args=[self.game.pk]),
            {'quantity': 2, 'redirect_url': '/'}
            )

        response = self.client.post(
            reverse('adjust_basket', args=[self.game.pk]),
            {'quantity': 3}
            )

        self.assertEqual(response.status_code, 302)

        # Check if the quantity of the game in the basket was updated
        basket = self.client.session.get('basket', {})
        self.assertEqual(basket[str(self.game.pk)], 3)

        # Check if the success message is in the messages
        messages_list = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 2)
        self.assertEqual(
            messages_list[1].message,
            f'Updated {self.game.name} quantity to 3'
            )

    def test_adjust_basket_view_with_platform_quantity_greater_than_zero(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('add_to_basket', args=[self.game2.pk]),
            {'quantity': 2, 'redirect_url': '/'}
        )

        response = self.client.post(
            reverse('adjust_basket', args=[self.game2.pk]),
            {'quantity': 3}
        )

        self.assertEqual(response.status_code, 302)

        basket = self.client.session.get('basket', {})
        self.assertEqual(basket[str(self.game2.pk)], 3)

        messages_list = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 2)
        self.assertEqual(
            messages_list[1].message.strip(),
            f'Updated {self.game2.name} {self.game2.platform} quantity to 3'
        )

    def test_adjust_basket_view_quantity_zero(self):
        self.client.force_login(self.user)
        # Add game to the basket first
        response = self.client.post(
            reverse('add_to_basket', args=[self.game.pk]),
            {'quantity': 2, 'redirect_url': '/'}
            )

        # Adjust the basket game quantity to zero
        response = self.client.post(
            reverse('adjust_basket', args=[self.game.pk]),
            {'quantity': 0}
            )

        self.assertEqual(response.status_code, 302)

        # Check if the success message is in the messages
        messages_list = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 2)
        self.assertEqual(
            messages_list[1].message,
            f'Removed {self.game.name} from your basket'
            )

        basket = self.client.session.get('basket', {})
        # Assert that the basket is now empty
        self.assertEqual(basket, {})
        # Ensure the game ID is not in the basket after removal
        self.assertNotIn(str(self.game.pk), basket)

    def test_adjust_basket_view_with_platform_quantity_zero(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('add_to_basket', args=[self.game2.pk]),
            {'quantity': 2, 'redirect_url': '/'}
        )

        response = self.client.post(
            reverse('adjust_basket', args=[self.game2.pk]),
            {'quantity': 0}
        )

        self.assertEqual(response.status_code, 302)

        basket = self.client.session.get('basket', {})
        self.assertNotIn(str(self.game2.pk), basket)

        messages_list = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 2)
        self.assertEqual(
            messages_list[1].message,
            f'Removed {self.game2.name} {self.game2.platform} from your basket'
        )


class TestRemoveFromBasketView(TestCase):

    """
    The setUp method is used to create Game and Platform objects and
    set up a client.
    We have three test methods:
    test_remove_from_basket_view, test_remove_from_basket_view_with_platform
    and test_remove_from_basket_view_error.
    - In test_remove_from_basket_view, we add a game to the basket,
    make sure the game is in the basket remove the game from the basket,
    check that the game was removed and that the message
    generated is correct.
    - In test_remove_from_basket_view_with_platform, we test
    the same as in the previous method but this time with a game that
    has platform attribute to check the correct message is generated.
    - test_remove_from_basket_view_error, we add a game to the basket,
    make sure the game is in the basket, try to remove the game with an
    incorrect id, check that we get a 500 response code, that the error
    message generated is correct and that the game is still in the basket.
    """

    def setUp(self):
        self.client = Client()

        # Create a platform
        self.platform = Platform.objects.create(name='Test Platform')
        # Create a game for testing
        self.game = Game.objects.create(
            name='Test Game', description='This is a test game.',
            year='2023', price=Decimal('29.99'),
            available_in_other_consoles=False,
            trailer='https://www.youtube.com/watch?v=video-id'
            )
        # Create a second game with platform
        self.game2 = Game.objects.create(
            name='Test Game', description='This is a test game.',
            year='2023', price=Decimal('29.99'),
            platform=self.platform,
            available_in_other_consoles=False,
            trailer='https://www.youtube.com/watch?v=video-id'
            )

    def test_remove_from_basket_view(self):
        # Add the game to the basket
        response = self.client.post(
            reverse('add_to_basket', args=[self.game.pk]),
            {'quantity': 2, 'redirect_url': '/'}
            )

        # Ensure the game is in the basket
        self.assertIn(str(self.game.pk), self.client.session['basket'])

        # Call the remove_from_basket view
        response = self.client.post(
            reverse('remove_from_basket', args=[self.game.pk])
            )

        # Check the response status code
        self.assertEqual(response.status_code, 200)

        # Ensure the game is removed from the basket
        self.assertNotIn(str(self.game.pk), self.client.session['basket'])

        # Check if the success message is in the messages
        messages_list = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 2)
        self.assertEqual(
            messages_list[1].message,
            f'Removed {self.game.name} from your basket'
            )

    def test_remove_from_basket_view_with_platform(self):
        # Add the game to the basket
        response = self.client.post(
            reverse('add_to_basket', args=[self.game2.pk]),
            {'quantity': 2, 'redirect_url': '/'}
        )

        # Ensure the game is in the basket
        self.assertIn(str(self.game2.pk), self.client.session['basket'])

        # Call the remove_from_basket view
        response = self.client.post(
            reverse('remove_from_basket', args=[self.game2.pk])
        )

        # Check the response status code
        self.assertEqual(response.status_code, 200)

        # Ensure the game is removed from the basket
        self.assertNotIn(str(self.game2.pk), self.client.session['basket'])

        # Check if the success message is in the messages
        messages_list = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 2)
        self.assertEqual(
            messages_list[1].message,
            f'Removed {self.game2.name} {self.game2.platform} from your basket'
        )

    def test_remove_from_basket_view_error(self):
        # Add the game to the basket
        response = self.client.post(
            reverse('add_to_basket', args=[self.game.pk]),
            {'quantity': 2, 'redirect_url': '/'}
            )

        # Ensure the game is in the basket
        self.assertIn(str(self.game.pk), self.client.session['basket'])

        # Clear any existing messages
        self.client.get(reverse('basket_summary'))

        # Call the remove_from_basket view with an invalid game_id
        response = self.client.post(reverse('remove_from_basket', args=[9999]))

        # Check the response status code
        self.assertEqual(response.status_code, 500)

        # Check if the error message is in the messages
        messages_list = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertIn(
            'Error removing game: No Game matches the given query.',
            messages_list[0].message
            )

        # Ensure the game is still in the basket
        self.assertIn(str(self.game.pk), self.client.session['basket'])
