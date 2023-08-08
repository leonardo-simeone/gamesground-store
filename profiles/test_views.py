import unittest
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from checkout.models import Order
from .models import UserProfile
from .forms import UserProfileForm
from django.test import Client
from .views import *
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from decimal import Decimal


class TestProfileView(TestCase):

    """
    The setUp method is used to create a User object and to get
    a UserProfile object.
    We have three test methods: test_profile_view_get,
    test_profile_view_post_valid_form and test_profile_view_post_invalid_form.
    - In test_profile_view_get, we get the profile view, test that the
    success response code is got (200), test that the correct heading is in the
    content, test that no messages are generated which means no post requests
    and test that orders can be got from the user profile should there be any.
    - test_profile_view_post_valid_form, we create valid data to populate a
    user profile field, save the profile then test the correct template
    is used, success response code is got (200), the correct message is
    generated and that the UserProfile object with the valid data exists.
    - In test_profile_view_post_invalid_form, we test the same as in the
    previous test but this time with invalid data and test that the
    UserProfile object with the invalid data doesn't exist.
    """

    def setUp(self):
        self.factory = RequestFactory()
        # Set up the test client
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
            )
        self.user_profile = UserProfile.objects.get(user=self.user)
        self.url = ''

    def test_profile_view_get(self):
        request = self.factory.get(self.url)
        request.user = self.user
        # Set up the session
        request.session = self.client.session

        response = profile(request)

        self.assertEqual(response.status_code, 200)
        # Check for the presence of a h2 element with 'My Profile' as content
        self.assertContains(
            response, '<h2 class="mb-4">My Profile</h2>', count=1
            )
        # Ensure error message is not present
        self.assertContains(
            response, 'Update failed. Please ensure the form is valid.',
            count=0
            )
        # Ensure success message is not present
        self.assertContains(response, 'Profile updated successfully', count=0)

        # Verify the orders associated with the user
        orders = Order.objects.filter(user_profile=self.user_profile)
        self.assertEqual(list(orders), list(self.user_profile.orders.all()))

    def test_profile_view_post_valid_form(self):
        # Valid data
        data = {'default_phone_number': '1234567890'}
        request = self.factory.post(self.url, data)
        request.user = self.user
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request._messages = FallbackStorage(request)

        # Checks the correct template is used, the correct response code
        # is got, the correct message is generated and the valid data is saved
        with self.assertTemplateUsed('profiles/profile.html'):
            response = profile(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, 'Profile updated successfully'
            )
        self.assertTrue(
            UserProfile.objects.filter(user=self.user, **data).exists()
            )

    def test_profile_view_post_invalid_form(self):
        # Invalid data
        data = {'default_phone_number': '123456789012345678901'}
        request = self.factory.post(self.url, data)
        request.user = self.user
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request._messages = FallbackStorage(request)

        # Checks the correct template is used, the correct response code
        # is got, the correct message is generated and the valid data
        # is not saved
        with self.assertTemplateUsed('profiles/profile.html'):
            response = profile(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, 'Update failed. Please ensure the form is valid.'
            )
        self.assertFalse(
            UserProfile.objects.filter(user=self.user, **data).exists()
            )


class TestOrderHistoryView(TestCase):

    """
    The setUp method is used to create an Order object.
    - In test_order_history, we get the order_history view
    using the newly created Order object and test that
    success response code is got (200), the correct template
    is used and that the view in fact contains the Order object
    attributes.
    """

    def setUp(self):
        # Create Order object
        self.order = Order.objects.create(
            order_number='59D52EBA7553416385A882EE642D7E0Z',
            full_name='Test User',
            email='test@test.com',
            phone_number='1234567890',
            country='Ireland',
            town_or_city='Test town',
            street_address1='Test address 1',
            date='July 28, 2023, 3:28 p.m.',
            delivery_cost=7.00,
            order_total=20.00,
            grand_total=27.00,
            )

    def test_order_history(self):

        # Get order_history view using the Order object
        response = self.client.get(
            reverse('order_history', args=[self.order.order_number])
            )

        # Test that response code, template used and attributes are correct
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')
        self.assertContains(response, '59D52EBA7553416385A882EE642D7E0Z')
        self.assertContains(response, 'Test User')
        self.assertContains(response, '1234567890')
        self.assertContains(response, 'test@test.com')
        self.assertEqual(self.order.grand_total, Decimal('27.00'))
