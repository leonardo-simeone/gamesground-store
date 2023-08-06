import unittest
from django.test import RequestFactory, TestCase, Client
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User, AnonymousUser
from unittest.mock import patch, Mock
from games.forms import GameForm
from games.models import *
from games.views import *
from decimal import Decimal


class TestGamesView(TestCase):

    """
    The setUp method is used to create Pegi, Platform and game objects.
    We have several test methods covering different
    aspects of the games view.
    - test_basic_view: Tests that the view contains the Game objects.
    - test_empty_query_redirects: Tests user will be redirected to games view
    and that en error message will be generated when the query content in
    the search bar is empty.
    - test_search_name: Tests search result of a game by name.
    - test_search_description: Tests search result of a game by description.
    - test_search_platform: Tests search result of a game by platform.
    - test_search_genre: Tests search result of a game by genre.
    - test_sorting_view: Tests sorting of games in this case by name.
    - test_filtering_view: Tests filtering of games in this case by platform.
    """

    def setUp(self):
        self.factory = RequestFactory()
        # Create Platform objects
        self.platform = Platform.objects.create(name='Platform 1')
        self.platform2 = Platform.objects.create(name='Platform 2')
        # Create Pegi object
        self.pegi_rating = Pegi.objects.create(age=18)
        # Create Game objects
        self.game1 = Game.objects.create(
            name='Test Game 1',
            platform=self.platform,
            pegi_rating=self.pegi_rating,
            genre='Action',
            year='2022',
            price=49.99,
            description='A test game',
            image=None,
            available_in_other_consoles=False,
            trailer='https://www.youtube.com/watch?v=video-id'
        )
        self.game2 = Game.objects.create(
            name='Test Game 2',
            platform=self.platform2,
            pegi_rating=self.pegi_rating,
            genre='Adventure',
            year='2022',
            price=49.99,
            description='Another test game',
            image=None,
            available_in_other_consoles=False,
            trailer='https://www.youtube.com/watch?v=video-id'
        )

    def mock_request(self, data=None):
        request = self.factory.get(reverse('games'), data)
        request.session = {}
        return request

    # Test games view
    def test_basic_view(self):
        request = self.mock_request()
        response = games(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Game 1')
        self.assertContains(response, 'Test Game 2')

    # Test response for an empty query
    @patch('games.views.messages')
    @patch('games.views.redirect')
    @patch('games.views.reverse')
    def test_empty_query_redirects(
        self, mock_reverse, mock_redirect, mock_messages
    ):
        mock_reverse.return_value = '/games/'
        mock_redirect.return_value = '/games/'
        mock_messages.error = Mock()

        request = self.mock_request({'q': ''})
        response = games(request)

        mock_reverse.assert_called_once_with('games')
        mock_redirect.assert_called_once_with('/games/')
        mock_messages.error.assert_called_once()

    # Test game search by name
    def test_search_name(self):
        request = self.mock_request({'q': 'Test'})
        response = games(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Game 1')
        self.assertNotContains(response, 'Another Game')

    # Test game search by description
    def test_search_description(self):
        request = self.mock_request({'q': 'Another'})
        response = games(request)

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Test Game 1')
        self.assertContains(response, 'Test Game 2')

    # Test game search by platform
    def test_search_platform(self):
        request = self.mock_request({'q': 'Platform 1'})
        response = games(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Game 1')
        self.assertNotContains(response, 'Test Game 2')

    # Test game search by genre
    def test_search_genre(self):
        request = self.mock_request({'q': 'Action'})
        response = games(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Game 1')
        self.assertNotContains(response, 'Test Game 2')

    # Test sorting game by name
    def test_sorting_view(self):
        request = self.mock_request({'sort': 'name', 'direction': 'asc'})
        response = games(request)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            response.content.index(b'Test Game 1')
            < response.content.index(b'Test Game 2')
            )

    # Test filtering game by platform
    def test_filtering_view(self):
        request = self.mock_request({'platform': 'Platform 1'})
        response = games(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Game 1')
        self.assertNotContains(response, 'Test Game 2')


class TestGameDetailView(TestCase):

    """
    The setUp method is used to create Pegi, Platform, Game and User objects.
    We have three test methods: test_game_detail_authenticated_liked,
    test_game_detail_authenticated_not_liked and
    test_game_detail_unauthenticated.
    - In test_game_detail_authenticated_liked, we login a user,
    like the game and render the game including the total_likes = 1.
    - In test_game_detail_authenticated_not_liked, we login a user,
    and not liking the game we render the game including the total_likes = 0.
    - In test_game_detail_unauthenticated, we simply render the game with all
    its attributes and no likes, total_likes = 0.
    """

    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
            )
        # Create pegi and platform
        self.pegi = Pegi.objects.create(age=18)
        self.platform = Platform.objects.create(name='Test Platform')
        # Create a game
        self.game = Game.objects.create(
            name='Test Game',
            genre='Action',
            description='This is a test game.',
            year='2023',
            platform=self.platform,
            price=49.99,
            pegi_rating=self.pegi,
            image=None,
            available_in_other_consoles=False,
            trailer='https://www.youtube.com/watch?v=video-id'
        )

    def test_game_detail_authenticated_liked(self):
        # Simulate an authenticated user who has liked the game
        self.client.force_login(self.user)
        self.game.likes.add(self.user)

        response = self.client.get(reverse('game_detail', args=[self.game.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Game')
        self.assertContains(response, 'This is a test game.')
        self.assertEqual(self.game.total_likes(), 1)

    def test_game_detail_authenticated_not_liked(self):
        # Simulate an authenticated user who has not liked the game
        self.client.force_login(self.user)

        response = self.client.get(reverse('game_detail', args=[self.game.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Game')
        self.assertContains(response, 'This is a test game.')
        self.assertEqual(self.game.total_likes(), 0)

    def test_game_detail_unauthenticated(self):
        # Simulate an unauthenticated user
        response = self.client.get(reverse('game_detail', args=[self.game.pk]))

        # Test a game can be viewed by unauthenticated user
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Game')
        self.assertContains(response, 'Action')
        self.assertContains(response, 'This is a test game.')
        self.assertContains(response, '2023')
        self.assertContains(response, 'Test Platform')
        self.assertContains(response, '49.99')
        self.assertContains(response, 'Ages 18 and over')
        self.assertTrue(
            response, (self.game.available_in_other_consoles is False)
            )
        self.assertTrue(response, (self.game.image is None))
        self.assertTrue(
            response, (
                self.game.trailer == 'https://www.youtube.com/watch?v=video-id'
                )
            )
        self.assertTrue(response, (self.game.total_likes() == 0))


class TestLikeGameView(TestCase):

    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
            )
        # Create pegi and platform
        self.pegi = Pegi.objects.create(age=18)
        self.platform = Platform.objects.create(name='Test Platform')
        # Create a game
        self.game = Game.objects.create(
            name='Test Game',
            genre='Action',
            description='This is a test game.',
            year='2023',
            platform=self.platform,
            price=49.99,
            pegi_rating=self.pegi,
            image=None,
            available_in_other_consoles=False,
            trailer='https://www.youtube.com/watch?v=video-id'
        )

    def test_like_game(self):
        # Tests that a Game can be liked when a POST request is made to it
        # and that it redirects successfully to game_detail URL.
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(
            reverse('like_game', args=[self.game.id]),
            {'game_id': self.game.id}
            )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url, reverse('game_detail', args=[self.game.id])
            )

        # Tests that the game was liked
        self.game.refresh_from_db()
        self.assertTrue(self.game.likes.filter(id=self.user.id).exists())

        # Tries to like the game again (Unlike)
        response = self.client.post(
            reverse('like_game', args=[self.game.id]),
            {'game_id': self.game.id}
            )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url, reverse('game_detail', args=[self.game.id])
            )

        # Tests that the game was unliked
        self.game.refresh_from_db()
        self.assertFalse(self.game.likes.filter(id=self.user.id).exists())


class TestAddGameView(TestCase):

    """
    The setUp method is used to create two User objects, one superuser
    and one regular user.
    We have several test methods covering different
    aspects of the add_game view.
    - test_add_game_authenticated_superuser_get: Tests superuser's GET request.
    - test_add_game_authenticated_superuser_post_valid_form: Tests superuser's
    POST request with a valid form.
    - test_add_game_authenticated_superuser_post_invalid_form: Tests
    superuser's POST request with an invalid form.
    - test_add_game_authenticated_non_superuser: Tests authenticated
    non-superuser's GET request.
    - test_add_game_unauthenticated: Tests unauthenticated user's GET request.
    """

    def setUp(self):
        self.client = Client()
        # Create a superuser
        self.superuser = User.objects.create_superuser(
            username='admin',
            password='adminpassword',
            email='admin@example.com'
            )
        # Create a regular user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
            )

    def test_add_game_authenticated_superuser_get(self):
        # Simulate an authenticated superuser's GET request
        self.client.force_login(self.superuser)

        response = self.client.get(reverse('add_game'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'games/add_game.html')
        self.assertIsInstance(response.context['form'], GameForm)

    def test_add_game_authenticated_superuser_post_valid_form(self):
        # Simulate an authenticated superuser's POST request with a valid form
        self.client.force_login(self.superuser)

        form_data = {
            'name': 'New Game',
            'description': 'This is a new game.',
            'year': '2023',
            'price': 49.99,
            'available_in_other_consoles': False,
            'trailer': 'https://www.youtube.com/watch?v=video-id'
        }

        response = self.client.post(
            reverse('add_game'), data=form_data, follow=True
            )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'games/game_detail.html')
        self.assertTrue(Game.objects.filter(name='New Game').exists())
        self.assertContains(response, 'Successfully added game!')

    def test_add_game_authenticated_superuser_post_invalid_form(self):
        # Simulate an authenticated superuser's POST
        # request with an invalid form
        self.client.force_login(self.superuser)
        # Create pegi and platform
        self.pegi = Pegi.objects.create(age=18)
        self.platform = Platform.objects.create(name='Test Platform')

        # name field is intentionally left blank
        # to trigger form validation error
        form_data = {
            'name': '',
            'description': 'Invalid game.',
            'genre': 'Action',
            'year': '2023',
            'platform': self.platform,
            'price': '49.99',
            'pegi_rating': self.pegi,
            'image': 'no image',
            'available_in_other_consoles': False,
            'trailer': 'https://www.youtube.com/watch?v=video-id'
        }

        response = self.client.post(
            reverse('add_game'), data=form_data, follow=True
            )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'games/add_game.html')
        self.assertContains(
            response, 'Failed to add game. Please ensure the form is valid.'
            )
        self.assertFalse(
            Game.objects.filter(description='Invalid game.').exists()
            )

    def test_add_game_authenticated_non_superuser(self):
        # Simulate an authenticated non-superuser's request
        self.client.force_login(self.user)

        response = self.client.get(reverse('add_game'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(len(messages.get_messages(response.wsgi_request)), 1)
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(
            messages_list[0].message, 'Sorry, only store owners can do that.'
            )

    def test_add_game_unauthenticated(self):
        # Simulate an unauthenticated user's request
        response = self.client.get(reverse('add_game'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse('account_login') + '?next=' + reverse('add_game')
            )


class TestEditGameView(TestCase):

    """
    The setUp method is used to create two User objects, one superuser
    and one regular user and a Game object.
    We have several test methods covering different
    aspects of the edit_game view.
    - test_edit_game_authenticated_superuser_get: Tests superuser's GET
    request.
    - test_edit_game_authenticated_superuser_post_valid_form: Tests superuser's
    POST request with a valid form.
    - test_edit_game_authenticated_superuser_post_invalid_form: Tests
    superuser's POST request with an invalid form.
    - test_edit_game_authenticated_non_superuser: Tests authenticated
    non-superuser's GET request.
    - test_edit_game_unauthenticated: Tests unauthenticated user's GET request.
    """

    def setUp(self):
        # Create a superuser
        self.superuser = User.objects.create_superuser(
            username='admin',
            password='adminpassword',
            email='admin@example.com'
            )
        # Create a regular user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
            )
        # Create a game
        self.game = Game.objects.create(
            name='Test Game',
            description='This is a test game.',
            year='2023',
            price=29.99,
            available_in_other_consoles=False,
            trailer='https://www.youtube.com/watch?v=video-id'
            )

    def test_edit_game_authenticated_superuser_get(self):
        # Simulate an authenticated superuser's GET request to edit a game
        self.client.force_login(self.superuser)

        response = self.client.get(reverse('edit_game', args=[self.game.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'games/edit_game.html')
        self.assertIsInstance(response.context['form'], GameForm)
        self.assertEqual(response.context['game'], self.game)

    def test_edit_game_authenticated_superuser_post_valid_form(self):
        # Simulate an authenticated superuser's POST request
        # to edit a game with a valid form
        self.client.force_login(self.superuser)

        form_data = {
            'name': 'Updated Game',
            'description': 'This is an updated game.',
            'year': '2022',
            'price': 39.99,
            'available_in_other_consoles': True,
            'trailer': 'https://www.youtube.com/watch?v=video-id',
        }

        response = self.client.post(
            reverse('edit_game', args=[self.game.pk]),
            data=form_data, follow=True
            )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'games/game_detail.html')

        # Refresh the game object from the database
        self.game.refresh_from_db()

        # Check if the game fields have been updated correctly
        self.assertEqual(self.game.name, 'Updated Game')
        self.assertEqual(self.game.description, 'This is an updated game.')
        self.assertEqual(self.game.year, '2022')
        self.assertEqual(self.game.price, Decimal('39.99'))
        self.assertTrue(self.game.available_in_other_consoles)
        self.assertEqual(
            self.game.trailer, 'https://www.youtube.com/watch?v=video-id'
            )

        # Check if a success message is in the response
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(
            messages_list[0].message, 'Successfully updated game!'
            )

    def test_edit_game_authenticated_superuser_post_invalid_form(self):
        # Simulate an authenticated superuser's POST request
        # to edit a game with an invalid form
        self.client.force_login(self.superuser)

        form_data = {
            # name field is intentionally left blank
            # to trigger form validation error
            'name': '',
            'description': 'Invalid updated game.',
            'year': '2022',
            'price': 39.99,
            'available_in_other_consoles': True,
            'trailer': 'http://updated.example.com',
        }

        response = self.client.post(
            reverse('edit_game', args=[self.game.pk]),
            data=form_data, follow=True
            )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'games/edit_game.html')
        self.assertContains(
            response, 'Failed to update game. Please ensure the form is valid.'
            )

        # Refresh the game object from the database
        self.game.refresh_from_db()

        # Check if the game fields remain unchanged
        self.assertEqual(self.game.name, 'Test Game')
        self.assertEqual(self.game.description, 'This is a test game.')
        self.assertEqual(self.game.year, '2023')
        self.assertEqual(self.game.price,  Decimal('29.99'))
        self.assertFalse(self.game.available_in_other_consoles)
        self.assertEqual(
            self.game.trailer, 'https://www.youtube.com/watch?v=video-id'
            )

    def test_edit_game_authenticated_non_superuser(self):
        # Simulate an authenticated non-superuser's request to edit a game
        self.client.force_login(self.user)

        response = self.client.get(reverse('edit_game', args=[self.game.pk]))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(len(messages.get_messages(response.wsgi_request)), 1)
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(
            messages_list[0].message, 'Sorry, only store owners can do that.'
            )

    def test_edit_game_unauthenticated(self):
        # Simulate an unauthenticated user's request to edit a game
        response = self.client.get(reverse('edit_game', args=[self.game.pk]))

        self.assertEqual(response.status_code, 302)

        login_url = reverse('account_login')
        edit_game_url = reverse('edit_game', args=[self.game.pk])
        redirect_url = login_url + '?next=' + edit_game_url

        self.assertRedirects(response, redirect_url)


class TestDeleteGameView(TestCase):

    """
    The setUp method is used to create two User objects, one superuser
    and one regular user and a Game object.
    We have several test methods covering different
    aspects of the delete_game view.
    - test_delete_game_authenticated_superuser_get: Tests superuser's GET
    request to delete a game.
    - test_delete_game_authenticated_superuser_post: Tests superuser's
    POST request to delete a game.
    - test_delete_game_authenticated_non_superuser: Tests authenticated
    non-superuser's GET request to delete a game.
    - test_delete_game_unauthenticated: Tests unauthenticated user's
    GET request to delete a game.
    """

    def setUp(self):
        # Create a superuser
        self.superuser = User.objects.create_superuser(
            username='admin',
            password='adminpassword',
            email='admin@example.com'
            )
        # Create a regular user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
            )
        # Create a game
        self.game = Game.objects.create(
            name='Test Game',
            description='This is a test game.',
            year='2023', price=29.99,
            available_in_other_consoles=False,
            trailer='https://www.youtube.com/watch?v=video-id'
            )

    def test_delete_game_authenticated_superuser_get(self):
        # Simulate an authenticated superuser's GET request to delete a game
        self.client.force_login(self.superuser)

        response = self.client.get(reverse('delete_game', args=[self.game.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'games/delete_game.html')
        self.assertEqual(response.context['game'], self.game)

    def test_delete_game_authenticated_superuser_post(self):
        # Simulate an authenticated superuser's POST request to delete a game
        self.client.force_login(self.superuser)

        response = self.client.post(
            reverse('delete_game', args=[self.game.pk]), follow=True
            )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'games/games.html')

        # Check if the game was deleted
        self.assertFalse(Game.objects.filter(pk=self.game.pk).exists())

        # Check if a success message is in the response
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(
            messages_list[0].message, f'{self.game.name} has been deleted!'
            )

    def test_delete_game_authenticated_non_superuser(self):
        # Simulate an authenticated non-superuser's request to delete a game
        self.client.force_login(self.user)

        response = self.client.get(reverse('delete_game', args=[self.game.pk]))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(len(messages.get_messages(response.wsgi_request)), 1)
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(
            messages_list[0].message, 'Sorry, only store owners can do that.'
            )

    def test_delete_game_unauthenticated(self):
        # Simulate an unauthenticated user's request to delete a game
        response = self.client.get(reverse('delete_game', args=[self.game.pk]))

        self.assertEqual(response.status_code, 302)

        login_url = reverse('account_login')
        delete_game_url = reverse('delete_game', args=[self.game.pk])
        redirect_url = login_url + '?next=' + delete_game_url

        self.assertRedirects(response, redirect_url)
