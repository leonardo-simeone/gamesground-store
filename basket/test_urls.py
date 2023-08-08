from django.urls import reverse
from django.test import TestCase
from django.contrib.messages import get_messages
from games.models import Game
from .views import basket_summary
from decimal import Decimal


class TestBasketUrls(TestCase):

    """
    The setUp method is used to create a Game object.
    We have several test methods covering different
    aspects of the basket urls.
    - test_basket_summary_url: Tests that when the view is called
    the response code (200 = success) and the template used are correct.
    - test_add_to_basket_url: Tests that when a game is added the redirect
    response code (302) and the redirect view are correct and that the success
    message is generated.
    - test_adjust_basket_url: Tests that when the view is called
    the redirect response code (302) and the redirect view are correct,
    and that the game quantity was adjusted accordingly.
    - test_remove_from_basket_url: Adds a game to the basket then checks
    that the game is in the basket then then tests that when the
    remove_from_basket view is called the response code (200 = success)
    is correct, the game is removed from the basket and that the success
    message is generated.
    """

    def setUp(self):
        # Create a test game
        self.game = Game.objects.create(
            name='Test Game', description='This is a test game.',
            year='2023', price=Decimal('29.99'),
            available_in_other_consoles=False,
            trailer='https://www.youtube.com/watch?v=video-id'
            )

    def test_basket_summary_url(self):
        response = self.client.get(reverse('basket_summary'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'basket/basket.html')

    def test_add_to_basket_url(self):
        response = self.client.post(
            reverse('add_to_basket', args=[self.game.pk]),
            {'quantity': 1, 'redirect_url': reverse('basket_summary')}
            )
        # Redirect after adding to basket
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('basket_summary'))

        # Check if the game is in the basket
        self.assertIn(str(self.game.pk), self.client.session['basket'])

        # Check for success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].level_tag, 'success')

    def test_adjust_basket_url(self):
        response = self.client.post(
            reverse('adjust_basket', args=[self.game.pk]),
            {'quantity': 2}
            )
        # Redirect after adjusting basket
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('basket_summary'))

        # Check if the quantity is adjusted
        self.assertEqual(self.client.session['basket'][str(self.game.pk)], 2)

    def test_remove_from_basket_url(self):
        # Add the game to the basket first
        self.client.post(
            reverse('add_to_basket', args=[self.game.pk]),
            {'quantity': 1, 'redirect_url': reverse('basket_summary')}
            )

        # Ensure the game is in the basket
        self.assertIn(str(self.game.pk), self.client.session['basket'])

        response = self.client.post(
            reverse('remove_from_basket', args=[self.game.pk])
            )
        self.assertEqual(response.status_code, 200)

        # Check if the game is removed from the basket
        self.assertNotIn(str(self.game.pk), self.client.session['basket'])

        # Check for success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[1].level_tag, 'success')
