from django.test import TestCase
from django.urls import reverse, resolve
from . import views


class TestHomeUrls(TestCase):

    """
    We have five test methods: test_home_url, test_contact_url,
    test_contact_list_url_resolves, test_newsletter_url and
    test_about_us_url.
    For each test method (except for test_contact_list_url_resolves):
    - We use the reverse function to generate
    the URL for the given view name.
    - We use self.client.get(url) to perform a GET request
    to the generated URL.
    - We assert that the response status code is 200 (indicating success).
    - We use assertTemplateUsed to verify that the expected template
    is used for rendering the response.
    - test_contact_list_url_resolves uses a reverse function to get the url
    pattern and then resolves to get the function. We then assertEqual
    the function returned is the same as its defined view function.
    """

    def test_home_url(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')

    def test_contact_url(self):
        url = reverse('contact')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/contact.html')

    def test_contact_list_url_resolves(self):
        url = reverse('contact_list')
        self.assertEqual(resolve(url).func, views.contact_list)

    def test_newsletter_url(self):
        url = reverse('newsletter')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/newsletter.html')

    def test_about_us_url(self):
        url = reverse('about_us')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/about_us.html')
