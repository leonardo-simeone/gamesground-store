from django.test import TestCase
from .models import *
from django.contrib.auth.models import User
from django.urls import reverse


class TestPlatformModel(TestCase):

    """
    We have three test methods: test_str_method, test_name_max_length,
    and test_name_blank_field.
    - In test_str_method, we create a Platform object and test if
    the __str__ method returns the expected string representation.
    - In test_name_max_length, we create a Platform object with a name
    that reaches the maximum length defined by the model's
    max_length attribute. We then test if the name is correctly saved.
    - In test_name_blank_field, we create a Platform object without
    specifying a name. We then test if the default value of an
    empty string is assigned to the name field.
    """

    def test_str_method(self):
        platform = Platform.objects.create(name='Test Platform')
        self.assertEqual(str(platform), 'Test Platform')

    def test_name_max_length(self):
        platform = Platform.objects.create(name='A' * 254)
        self.assertEqual(platform.name, 'A' * 254)

    def test_name_blank_field(self):
        platform = Platform.objects.create()
        self.assertEqual(platform.name, '')


class TestPegiModel(TestCase):

    """
    We have three test methods: test_str_method,
    test_age_field, and test_verbose_name_plural.
    - In test_str_method, we create a Pegi object and
    test if the __str__ method returns the expected string
    representation.
    - In test_age_field, we create a Pegi object with a specific
    age and then test if the age field is correctly saved.
    - In test_verbose_name_plural, we test if the verbose_name_plural
    attribute of the Pegi model's Meta class is set to the expected value.
    """

    def test_str_method(self):
        pegi = Pegi.objects.create(age=18)
        self.assertEqual(str(pegi), 'Ages 18 and over')

    def test_age_field(self):
        pegi = Pegi.objects.create(age=12)
        self.assertEqual(pegi.age, 12)

    def test_verbose_name_plural(self):
        self.assertEqual(Pegi._meta.verbose_name_plural, 'Pegi Rating')


class TestGameModel(TestCase):

    """
    The setUp method is used to create User, Pegi and Platform objects.
    We have several test methods covering different
    aspects of the Game model.
    - test_str_method: Tests the __str__ method of the Game model.
    - test_total_likes: Tests the total_likes method of the Game model.
    - test_game_creation: Tests the creation and attributes of a Game object.
    - test_games_view: Tests the games view (games) using Django's test client.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.pegi = Pegi.objects.create(age=18)
        self.platform = Platform.objects.create(name='Test Platform')

    def test_str_method(self):
        game = Game.objects.create(
            name='Test Game',
            genre=['Action', 'Adventure'],
            description='This is a test game.',
            year='2023',
            platform=self.platform,
            price=49.99,
            pegi_rating=self.pegi,
            image=None,
            available_in_other_consoles=False,
            trailer='https://www.youtube.com/watch?v=video-id'
        )
        self.assertEqual(str(game), 'Test Game Test Platform')

    def test_total_likes(self):
        game = Game.objects.create(
            name='Test Game',
            description='This is a test game.',
            year='2023',
            platform=self.platform,
            price=49.99,
            pegi_rating=self.pegi,
            trailer='https://www.youtube.com/watch?v=video-id'
        )
        game.likes.add(self.user)
        self.assertEqual(game.total_likes(), 1)

    def test_game_creation(self):
        game = Game.objects.create(
            name='Test Game',
            genre=['Action', 'Adventure'],
            description='This is a test game.',
            year='2023',
            platform=self.platform,
            price=49.99,
            pegi_rating=self.pegi,
            image=None,
            available_in_other_consoles=False,
            trailer='https://www.youtube.com/watch?v=video-id'
        )
        self.assertTrue(isinstance(game, Game))
        self.assertEqual(game.__str__(), game.name + ' ' + game.platform.name)
        self.assertEqual(game.total_likes(), 0)
        self.assertEqual(game.likes.count(), 0)

    def test_games_view(self):
        url = reverse('games')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'games/games.html')
