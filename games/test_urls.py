from django.test import TestCase
from django.urls import reverse, resolve
from . import views


class TestGamesURL(TestCase):

    """
    We have several test methods covering different URL patterns:
    - test_games_url: Tests if the URL pattern for the 'games'
    view is correctly mapped.
    - test_game_detail_url: Tests if the URL pattern for the
    'game_detail' view is correctly mapped.
    - test_like_game_url: Tests if the URL pattern for the
    'like_game' view is correctly mapped.
    - test_add_game_url: Tests if the URL pattern for the 'add_game'
    view is correctly mapped.
    - test_edit_game_url: Tests if the URL pattern for the
    'edit_game' view is correctly mapped.
    - test_delete_game_url: Tests if the URL pattern for the 'delete_game'
    view is correctly mapped.
    """

    def test_games_url(self):
        url = reverse('games')
        self.assertEqual(resolve(url).func, views.games)

    def test_game_detail_url(self):
        game_id = 1
        url = reverse('game_detail', args=[game_id])
        self.assertEqual(resolve(url).func, views.game_detail)

    def test_like_game_url(self):
        game_id = 1
        url = reverse('like_game', args=[game_id])
        self.assertEqual(resolve(url).func, views.like_game)

    def test_add_game_url(self):
        url = reverse('add_game')
        self.assertEqual(resolve(url).func, views.add_game)

    def test_edit_game_url(self):
        game_id = 1
        url = reverse('edit_game', args=[game_id])
        self.assertEqual(resolve(url).func, views.edit_game)

    def test_delete_game_url(self):
        game_id = 1
        url = reverse('delete_game', args=[game_id])
        self.assertEqual(resolve(url).func, views.delete_game)
