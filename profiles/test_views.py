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
from django.contrib import messages
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth import get_user_model
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
    The setUp method is used to create User and Order objects.
    We have two test methods: test_order_history_own_user and
    test_order_history_other_user.
    - In test_order_history_own_user, we login user a which owns order a,
    get the order_history view using the newly created Order object
    and test that success response code is got (200), the correct template
    is used and that the view in fact contains the Order object attributes.
    - In test_order_history_other_user, we login user a which doesn't own
    order b, try to get the order_history view for order b and check that the
    response code got is correct (302), that the user is redirected to the
    home page and that the message generated is correct.
    """

    def setUp(self):
        # Create User objects
        self.user_a = get_user_model().objects.create_user(
            username='user_a',
            password='password'
        )
        self.user_b = get_user_model().objects.create_user(
            username='user_b',
            password='password'
        )

        # Create UserProfile objects for both users
        self.user_profile_a = self.user_a.userprofile
        self.user_profile_b = self.user_b.userprofile

        # Create Order objects for both users
        self.order_a = Order.objects.create(
            order_number='59D52EBA7553416385A882EE642D7E0X',
            user_profile=self.user_a.userprofile,
            full_name='Test User A',
            email='test_a@test.com',
            phone_number='1234567890',
            country='Ireland',
            town_or_city='Test town A',
            street_address1='Test address 1',
            date='July 28, 2023, 3:28 p.m.',
            delivery_cost=7.00,
            order_total=20.00,
            grand_total=27.00,
        )

        self.order_b = Order.objects.create(
            order_number='59D52EBA7553416385A882EE642D7E0Y',
            user_profile=self.user_b.userprofile,
            full_name='Test User B',
            email='test_b@test.com',
            phone_number='9876543210',
            country='USA',
            town_or_city='Test town B',
            street_address1='Test address 2',
            date='July 28, 2023, 3:28 p.m.',
            delivery_cost=10.00,
            order_total=30.00,
            grand_total=40.00,
        )

    def test_order_history_own_user(self):
        # Login user A
        self.client.login(username='user_a', password='password')

        # Access order history view for user A's order
        response = self.client.get(
            reverse('order_history', args=[self.order_a.order_number])
        )

        # Test that response code, template used, and attributes are correct
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')
        self.assertContains(response, '59D52EBA7553416385A882EE642D7E0X')
        self.assertContains(response, 'Test User A')
        self.assertContains(response, '1234567890')
        self.assertContains(response, 'test_a@test.com')
        self.assertEqual(self.order_a.grand_total, Decimal('27.00'))

    def test_order_history_other_user(self):
        # Login user A
        self.client.login(username='user_a', password='password')

        # Try to access order history view for user B's order
        response = self.client.get(
            reverse('order_history', args=[self.order_b.order_number])
        )

        # Test that response status code indicates redirection
        self.assertEqual(response.status_code, 302)

        # Test that the user is redirected to the home page
        self.assertRedirects(response, reverse('home'))

        # Follow the redirection and test the messages on the redirected page
        redirected_response = self.client.get(response.url, follow=True)
        # Test that the expected error message is correct
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(
            messages_list[0].message, 'You do not have permission to view '
            'this order history.'
            )
