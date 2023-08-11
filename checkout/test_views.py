from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from decimal import Decimal
from unittest.mock import patch, Mock
from checkout.views import *
from checkout.forms import OrderForm
from profiles.forms import UserProfileForm
from checkout.models import Order, OrderLineGame
from checkout.views import checkout_success
from profiles.models import UserProfile
from basket.contexts import basket_contents
from games.models import *
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.storage.fallback import FallbackStorage
from django.core import mail


class TestCheckoutView(TestCase):

    """
    The setUp method is used to create Pegi, Platform, Game and User objects,
    get the user profile and to define the basket contents.
    We have several test methods covering different aspects of the
    checkout view.
    - test_checkout_view_get_anonymous_user: Tests an anonymous user can get
    the checkout view.
    - test_checkout_view_get_authenticated_user: Tests an authenticated user
    can get the checkout view.
    - test_checkout_view_post_valid_form_anonymous_user: Tests an anonymous
    user can complete checkout with valid form data.
    - test_checkout_view_post_valid_form_authenticated_user: Tests an
    authenticated user can complete checkout with valid form data.
    - test_game_not_found: Tests that the response in case of game not existent
    in the database is correct (response code, url and error message).
    - test_user_profile_not_found: Tests that the response in case of user
    profile not existent in the database is correct
    (response code).
    Since the intent object is directly referenced in a possible
    test_checkout_view_post_invalid_form method, and the view
    structure heavily depends on it, it seems difficult to test
    the view for post invalid data without involving the Stripe API
    or modifying the view.
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
            )
        self.pegi = Pegi.objects.create(age=18)
        self.platform = Platform.objects.create(name='Test Platform')
        self.game = Game.objects.create(
            name='Test Game',
            genre=['Action', 'Adventure'],
            description='This is a test game.',
            year='2023',
            platform=self.platform,
            price=Decimal('25.00'),
            pegi_rating=self.pegi,
            image=None,
            available_in_other_consoles=False,
            trailer='https://www.youtube.com/watch?v=video-id'
            )
        self.basket = {'1': 2}
        self.profile = UserProfile.objects.get(user=self.user)

    # Test get checkout view with anonymous user
    def test_checkout_view_get_anonymous_user(self):
        request = self.factory.get(reverse('checkout'))
        request.session = {'basket': self.basket}
        request.user = AnonymousUser()

        response = checkout(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<input type="text" name="full_name"')
        self.assertContains(response, '<h2 class="mb-4">Checkout</h2>')
        self.assertContains(response, 'Test Game')
        self.assertContains(response, self.game.platform)
        self.assertContains(response, 25)

    # Test get checkout view with authenticated user
    def test_checkout_view_get_authenticated_user(self):
        request = self.factory.get(reverse('checkout'))
        request.session = {'basket': self.basket}
        request.user = self.user
        self.profile = UserProfile.objects.get(user=self.user)

        response = checkout(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user.username, str(self.profile))
        self.assertIsNone(self.profile.default_phone_number)
        self.assertIsNone(self.profile.default_street_address1)
        self.assertIsNone(self.profile.default_street_address2)
        self.assertIsNone(self.profile.default_town_or_city)
        self.assertIsNone(self.profile.default_county)
        self.assertIsNone(self.profile.default_postcode)
        self.assertEqual(self.profile.default_country, None)
        self.assertContains(response, '<input type="text" name="full_name"')
        self.assertContains(response, '<h2 class="mb-4">Checkout</h2>')
        self.assertContains(response, 'Test Game')
        self.assertContains(response, self.game.platform)
        self.assertContains(response, 25)

    # Test checkout valid form with anonymous user
    @patch('checkout.views.stripe.PaymentIntent.create')
    def test_checkout_view_post_valid_form_anonymous_user(
         self, mock_stripe_payment_intent):
        force_order_number = '56E3AC1F12814832AB8397205867DCB4'
        request = self.factory.post(reverse('checkout'), {
            'full_name': 'Test User',
            'email': 'test@example.com',
            'phone_number': '1234567890',
            'country': 'US',
            'postcode': '12345',
            'town_or_city': 'Test City',
            'street_address1': '123 Test St',
            'street_address2': 'Apt 2',
            'county': 'Test County',
        })
        request.session = {'basket': self.basket}
        request.user = AnonymousUser()

        with patch(
            'checkout.models.Order._generate_order_number',
             return_value=force_order_number):
            response = checkout(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            reverse('checkout_success', args=[force_order_number]))

        order = Order.objects.last()
        self.assertEqual(order.full_name, 'Test User')
        self.assertEqual(order.order_number, force_order_number)

        order_line_game = OrderLineGame.objects.last()
        self.assertEqual(order_line_game.game, self.game)
        self.assertEqual(order_line_game.quantity, 2)

    # Test checkout valid form with authenticated user
    @patch('checkout.views.stripe.PaymentIntent.create')
    def test_checkout_view_post_valid_form_authenticated_user(
         self, mock_stripe_payment_intent):
        force_order_number = '56E3AC1F12814832AB8397205867DCB4'
        request = self.factory.post(reverse('checkout'), {
            'full_name': 'Test User',
            'email': 'test@example.com',
            'phone_number': '1234567890',
            'country': 'US',
            'postcode': '12345',
            'town_or_city': 'Test City',
            'street_address1': '123 Test St',
            'street_address2': 'Apt 2',
            'county': 'Test County',
        })
        request.session = {'basket': self.basket}
        request.user = self.user

        with patch(
            'checkout.models.Order._generate_order_number',
             return_value=force_order_number):
            response = checkout(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            reverse('checkout_success', args=[force_order_number]))

        order = Order.objects.last()
        self.assertEqual(order.full_name, 'Test User')
        self.assertEqual(order.order_number, force_order_number)

        order_line_game = OrderLineGame.objects.last()
        self.assertEqual(order_line_game.game, self.game)
        self.assertEqual(order_line_game.quantity, 2)

    @patch('checkout.views.messages')
    @patch('games.views.Game.objects.get')
    def test_game_not_found(self, mock_game_get, mock_messages):
        # Mock Game.objects.get to raise Game.DoesNotExist exception
        mock_game_get.side_effect = Game.DoesNotExist()

        request = self.factory.post(reverse('checkout'), {
            'full_name': 'John Doe',
            'email': 'john@example.com',
            'phone_number': '1234567890',
            'country': 'US',
            'postcode': '12345',
            'town_or_city': 'Test City',
            'street_address1': '123 Test St',
            'street_address2': 'Apt 2',
            'county': 'Test County',
        })

        request.session = {'basket': {'1': 2}}  # Sample basket data
        request.user = self.user
        request._messages = FallbackStorage(request)

        response = checkout(request)

        # Assert that the response is a redirect
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('basket_summary'))

        # Assert that the correct message was added to the messages
        mock_messages.error.assert_called_once()

    @patch('profiles.views.UserProfile.objects.get')
    def test_user_profile_not_found(self, mock_user_profile_get):
        # Mock UserProfile.objects.get
        # to raise UserProfile.DoesNotExist exception
        mock_user_profile_get.side_effect = UserProfile.DoesNotExist()

        request = self.factory.post(reverse('checkout'), {
            'full_name': 'John Doe',
            'email': 'john@example.com',
            'phone_number': '1234567890',
            'country': 'US',
            'postcode': '12345',
            'town_or_city': 'Test City',
            'street_address1': '123 Test St',
            'street_address2': 'Apt 2',
            'county': 'Test County',
        })

        # Sample basket data
        request.session = {'basket': {'1': 2}}
        request.user = self.user

        response = checkout(request)

        # Assert that the response is successful
        self.assertEqual(response.status_code, 302)


class TestCheckoutSuccessView(TestCase):

    """
    The setUp method is used to create Pegi, Platform, Game, User
    and Order objects, get the user profile and to define the basket
    contents.
    We have several test methods covering different aspects of the
    checkout success view.
    - test_checkout_success_authenticated_user: Tests that an authenticated
    user completed checkout successfully, checking for correct response
    code(200), template used, order number and email sent.
    - test_checkout_success_anonymous_user: Tests that an anonymous
    user completed checkout successfully, checking for correct response
    code(200), template used, order number and email sent.
    - test_checkout_success_basket_cleared: Tests that basket is cleared
    once checkout success is achieved.
    - test_checkout_success_messages: Tests that the correct message for the
    user is generated once checkout success is achieved.
    - test_checkout_success_email_sent: Tests that an email is sent to the user
    once checkout success is achieved, checking for instance the email subject.
    - test_checkout_success_template_context: Tests that the context in the
    checkout success view/template is correct.
    - test_checkout_success_template_used: Tests that the correct template
    is used for checkout success view.
    - test_save_user_info: Tests that when save_info equals True, the user
    info will be stored, we assert the response code is correct(200) and
    that the user info fields are correct for checkout_success.
    - test_basket_deleted: Tests that basket is deleted in checkout success.
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='test@test.com',
        )
        self.pegi = Pegi.objects.create(age=18)
        self.platform = Platform.objects.create(name='Test Platform')
        self.game = Game.objects.create(
            name='Test Game',
            genre=['Action', 'Adventure'],
            description='This is a test game.',
            year='2023',
            platform=self.platform,
            price=Decimal('25.00'),
            pegi_rating=self.pegi,
            image=None,
            available_in_other_consoles=False,
            trailer='https://www.youtube.com/watch?v=video-id'
            )
        self.profile = UserProfile.objects.get(user=self.user)
        self.basket = {'1': 2}
        self.order_number = '56E3AC1F12814832AB8397205867DCB4'
        self.order = Order.objects.create(
            order_number=self.order_number,
            full_name='Test User',
            email='test@example.com',
            phone_number='1234567890',
            country='US',
            postcode='12345',
            town_or_city='Test City',
            street_address1='123 Test St',
            street_address2='Apt 2',
            county='Test County',
        )

    def test_checkout_success_authenticated_user(self):
        request = self.factory.get(
            reverse('checkout_success', args=[self.order_number])
            )
        request.user = self.user
        request.session = {'basket': self.basket}

        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        with self.assertTemplateUsed('checkout/checkout_success.html'):
            response = checkout_success(request, self.order_number)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.order_number)
        # Check if email is sent
        self.assertEqual(len(mail.outbox), 1)

    def test_checkout_success_anonymous_user(self):
        request = self.factory.get(
            reverse('checkout_success', args=[self.order_number])
            )
        request.user = AnonymousUser()
        request.session = {'basket': self.basket}

        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        with self.assertTemplateUsed('checkout/checkout_success.html'):
            response = checkout_success(request, self.order_number)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.order_number)
        # Check if email is sent
        self.assertEqual(len(mail.outbox), 1)

    def test_checkout_success_basket_cleared(self):
        # Add 'basket' key to the session to simulate a previous checkout
        request = self.factory.get(
            reverse('checkout_success', args=[self.order_number])
            )
        request.user = self.user
        request.session = {'basket': self.basket}

        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = checkout_success(request, self.order_number)

        # Basket should be cleared
        self.assertNotIn('basket', request.session)

    def test_checkout_success_messages(self):
        # Create a test client
        client = Client()

        # Perform a GET request to simulate the checkout_success view
        response = client.get(
            reverse('checkout_success', args=[self.order.order_number])
            )

        # Check the response status code
        self.assertEqual(response.status_code, 200)

        # Check if messages are present in the response
        self.assertIn('messages', response.context)

        # Check if the messages framework works as expected
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertTrue(
            str(messages[0]).startswith('Order successfully processed!')
            )

        # Check the rendered template
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')

    def test_checkout_success_email_sent(self):
        request = self.factory.get(
            reverse('checkout_success', args=[self.order_number])
            )
        request.user = self.user

        # Manually create a session for the request
        session_middleware = SessionMiddleware()
        session_middleware.process_request(request)
        request.session.save()

        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = checkout_success(request, self.order_number)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Order successfully processed!')

        # Ensure only one email was sent
        self.assertEqual(len(mail.outbox), 1)

        sent_email = mail.outbox[0]
        self.assertEqual(
            sent_email.subject,
            f'Gamesground Store Confirmation for Order Number '
            f'{ self.order_number }'
            )
        self.assertEqual(sent_email.to, ['test@example.com'])

        # Clear the mail.outbox after the test
        mail.outbox = []

    def test_checkout_success_template_context(self):
        request = self.factory.get(
            reverse('checkout_success', args=[self.order_number])
            )
        request.user = self.user

        session_middleware = SessionMiddleware()
        session_middleware.process_request(request)
        request.session.save()

        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = checkout_success(request, self.order_number)

        self.assertContains(response, self.order_number)

    def test_checkout_success_template_used(self):
        request = self.factory.get(
            reverse('checkout_success', args=[self.order_number])
            )
        request.user = self.user

        session_middleware = SessionMiddleware()
        session_middleware.process_request(request)
        request.session.save()

        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        with self.assertTemplateUsed('checkout/checkout_success.html'):
            response = checkout_success(request, self.order_number)

        self.assertEqual(response.status_code, 200)

    @patch('checkout.views.messages')
    @patch('profiles.views.UserProfileForm')
    def test_save_user_info(
         self,
         mock_user_profile_form, mock_messages):
        # Mock form validation
        mock_user_profile_form.return_value.is_valid.return_value = True

        checkout_success_url = reverse(
            'checkout_success', args=['56E3AC1F12814832AB8397205867DCB5']
            )
        request = self.factory.get(checkout_success_url)
        request.user = self.user
        request.session = {'save_info': True}
        request._messages = FallbackStorage(request)

        self.order_number = '56E3AC1F12814832AB8397205867DCB5'
        self.order = Order.objects.create(
            order_number=self.order_number,
            full_name='Test User',
            email='test@example.com',
            phone_number='1234567890',
            country='US',
            postcode='12345',
            town_or_city='Test City',
            street_address1='123 Test St',
            street_address2='Apt 2',
            county='Test County',
        )
        response = checkout_success(
            request, '56E3AC1F12814832AB8397205867DCB5'
            )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.order.full_name)
        self.assertContains(response, self.order.email)
        self.assertContains(response, self.order.phone_number)

    def test_basket_deleted(self):
        request = self.factory.get('/')
        request.user = self.user
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        # Add a 'basket' to the session
        request.session['basket'] = self.basket
        request.session.save()

        # Apply MessageMiddleware
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        # Call the checkout_success view
        response = checkout_success(request, order_number=self.order_number)

        # Check if the 'basket' is deleted from the session
        self.assertNotIn('basket', request.session)
