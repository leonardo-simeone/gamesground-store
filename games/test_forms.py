from django.test import TestCase
from .models import *
from .forms import GameForm


class TestGameForm(TestCase):

    """
    We have several test methods covering different
    aspects of the GameForm form:
    - test_form_fields: Tests if the form has the expected fields.
    - test_form_field_widget_attributes: Tests if the widget attributes
    are set correctly for each form field.
    - test_form_choices: Tests if the choices for the platform
    and pegi_rating fields are set correctly.
    - test_form_valid_data: Tests the form with valid data
    and verifies if it is valid.
    - test_form_invalid_data: Tests the form with invalid data
    and verifies if it is invalid.
    """

    def setUp(self):
        self.platform = Platform.objects.create(name='Test Platform')
        self.pegi = Pegi.objects.create(age=18)

    def test_form_fields(self):
        form = GameForm()
        expected_fields = [
            'name', 'genre', 'description', 'year',
            'platform', 'price', 'pegi_rating', 'image',
            'available_in_other_consoles', 'trailer'
            ]
        self.assertCountEqual(form.fields.keys(), expected_fields)

    def test_form_field_widget_attributes(self):
        form = GameForm()
        self.assertEqual(form.fields['name'].widget.attrs['autofocus'], True)
        for field_name, field in form.fields.items():
            self.assertEqual(
                field.widget.attrs['class'], 'border-black rounded'
                )

    def test_form_choices(self):
        form = GameForm()

        platform_choices = form.fields['platform'].choices
        expected_platform_choices = [(self.platform.id, self.platform.name)]
        self.assertEqual(platform_choices, expected_platform_choices)

        pegi_choices = form.fields['pegi_rating'].choices
        expected_pegi_choices = [(self.pegi.id, self.pegi.age)]
        self.assertEqual(pegi_choices, expected_pegi_choices)

    def test_form_valid_data(self):
        form_data = {
            'name': 'Test Game',
            'genre': ['Action', 'Adventure'],
            'description': 'This is a test game.',
            'year': '2023',
            'platform': self.platform.id,
            'price': 49.99,
            'pegi_rating': self.pegi.id,
            'image': None,
            'available_in_other_consoles': False,
            'trailer': 'https://www.youtube.com/watch?v=video-id',
        }
        form = GameForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        form_data = {
            'name': '',
            'genre': ['Action', 'Adventure'],
            'description': 'This is a test game.',
            'year': '2023',
            'platform': self.platform.id,
            'price': 49.99,
            'pegi_rating': self.pegi.id,
            'image': None,
        }
        form = GameForm(data=form_data)
        self.assertFalse(form.is_valid())
