from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.shortcuts import render
from home.views import about_us
from .models import *
from .forms import *


class TestIndexView(TestCase):

    """
    We test the index view by using the reverse function to generate
    the URL for the 'home' view.
    We use self.client.get(url) to perform a GET request to the generated URL.
    We assert that the response status code is 200 (indicating success).
    We use assertTemplateUsed to verify that the expected template
    is used for rendering the response.
    """

    def test_index_view(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')


class TestContactView(TestCase):

    """
    We set up a Client to simulate GET and POST requests.
    We test the contact view for both GET and POST requests.
    We have three test methods: test_contact_view_get,
    test_contact_view_post_valid_form and test_contact_view_post_invalid_form
    - In the test_contact_view_get method, we assert that
    the response status code is 200, the expected template is used,
    and the context contains the form.
    - In the test_contact_view_post_valid_form method, we simulate
    a valid POST request, assert that the response
    status code is 302 (indicating a redirect), verify the correct
    redirect URL, check that a Contact object is created in the database,
    and verify the success message.
    - In the test_contact_view_post_invalid_form method, we simulate an
    invalid POST request, assert that the response status code is 200,
    verify the expected form errors, ensure no Contact object is created,
    and confirm that an error message is generated.
    """

    def setUp(self):
        self.client = Client()

    def test_contact_view_get(self):
        url = reverse('contact')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/contact.html')
        self.assertIsInstance(response.context['form'], ContactForm)

    def test_contact_view_post_valid_form(self):
        url = reverse('contact')
        data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'body': 'This is a test message.'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(Contact.objects.count(), 1)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), 'Thanks for contacting Gamesground!'
            )

    def test_contact_view_post_invalid_form(self):
        url = reverse('contact')
        data = {
            'name': 'Test User',
            'email': 'invalid_email',
            'body': ''
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/contact.html')
        self.assertFormError(
            response, 'form', 'email', 'Enter a valid email address.'
            )
        self.assertFormError(
            response, 'form', 'body', 'This field is required.'
            )
        self.assertEqual(Contact.objects.count(), 0)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)


class TestContactListView(TestCase):

    """
    We have two test methods: test_contact_list_view_not_superuser
    and test_contact_list_view_superuser.
    For each test method we set up a Client and a user with superuser
    privileges, and we log in with that user.
    - In test_contact_list_view_not_superuser, we modify the user's
    is_superuser attribute to False to simulate a non-superuser.
    We then try to access the contact_list view and verify that
    we're redirected to the home page with an error message.
    - In test_contact_list_view_superuser, we create a Contact object
    and then access the contact_list view. We verify that the
    response status code is 200, the expected template is used, and the
    context contains the contacts. We also check if the contact information
    is present in the response.
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass',
            is_superuser=True
        )
        self.client.login(username='testuser', password='testpass')

    def test_contact_list_view_not_superuser(self):
        self.user.is_superuser = False
        self.user.save()

        url = reverse('contact_list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), 'Sorry, only store owners can do that.'
            )

    def test_contact_list_view_superuser(self):
        Contact.objects.create(
            name='Test User',
            email='test@example.com',
            body='This is a test message.'
        )

        url = reverse('contact_list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/contact_list.html')

        contacts = response.context['contacts']
        self.assertEqual(contacts.count(), 1)

        self.assertContains(response, 'Test User')
        self.assertContains(response, 'test@example.com')
        self.assertContains(response, 'This is a test message.')


class TestNewsletterView(TestCase):

    """
    We have three test methods: test_newsletter_view_get,
    test_newsletter_view_post_valid_form, and
    test_newsletter_view_post_invalid_form.
    For each test method we set up a Client to simulate
    GET and POST requests.
    - In the test_newsletter_view_get method, we assert that
    the response status code is 200, the expected template is used,
    and the context contains the form.
    - In the test_newsletter_view_post_valid_form method, we simulate
    a valid POST request, assert that the response status code is 302
    (indicating a redirect), verify the correct redirect URL,
    check that a Newsletter object is created in the database,
    and verify the success message.
    - In the test_newsletter_view_post_invalid_form method, we simulate
    an invalid POST request, assert that the response status code is 200,
    verify the expected form error, ensure no Newsletter object is created,
    and confirm that an error message is generated.
    """

    def setUp(self):
        self.client = Client()

    def test_newsletter_view_get(self):
        url = reverse('newsletter')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/newsletter.html')
        self.assertIsInstance(response.context['form'], NewsletterForm)

    def test_newsletter_view_post_valid_form(self):
        url = reverse('newsletter')
        data = {
            'name': 'Test User',
            'email': 'test@example.com',
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(Newsletter.objects.count(), 1)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), 'Thanks for subscribing to our newsletter!'
            )

    def test_newsletter_view_post_invalid_form(self):
        url = reverse('newsletter')
        data = {
            'name': 'Test User',
            'email': 'invalid_email',
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/newsletter.html')
        self.assertFormError(
            response, 'form', 'email', 'Enter a valid email address.'
            )
        self.assertEqual(Newsletter.objects.count(), 0)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)


class TestAboutUsView(TestCase):

    """
    Tests that the response code is correct(200)
    and that the correct template is used.
    """

    def test_about_us_view(self):
        url = reverse('about_us')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/about_us.html')
