from django.test import TestCase
from django.contrib.auth.models import User
from django.http import HttpRequest
from .models import Contact
from home.contact_count import contacts_count_context


class TestContactCount(TestCase):

    """
    The setUp method is used to create a User object and
    make it SuperUser.
    - test_contacts_count_context: Tests that the context returned
    by the function is correct.
    """

    def setUp(self):
        # Create a test user with superuser privileges
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
            )
        self.user.is_superuser = True
        self.user.save()

    def test_contacts_count_context(self):
        # Create some test Contact objects
        Contact.objects.create(
            name='User 1', email='user1@example.com', body='Message 1'
            )
        Contact.objects.create(
            name='User 2', email='user2@example.com', body='Message 2'
            )

        # Simulate a request with the superuser
        request = HttpRequest()
        request.user = self.user

        # Call the context processor function
        context = contacts_count_context(request)

        # Check if the context variable is correctly provided
        self.assertIn('contacts_count', context)
        self.assertEqual(context['contacts_count'], 2)
