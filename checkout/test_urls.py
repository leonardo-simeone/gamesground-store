from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from .views import checkout, checkout_success


class TestCheckoutUrls(SimpleTestCase):

    """
    All methods test that the view gotten for each url are correct
    and that the urls paths are also correct.
    """

    def test_checkout_url_resolves(self):
        url = reverse('checkout')
        self.assertEqual(resolve(url).func, checkout)

    def test_checkout_success_url_resolves(self):
        url = reverse(
            'checkout_success',
            args=['59D52EBA7553416385A882EE642D7E0Z']
            )
        self.assertEqual(resolve(url).func, checkout_success)

    def test_checkout_url_name(self):
        url = reverse('checkout')
        self.assertEqual(url, '/checkout/')

    def test_checkout_success_url_name(self):
        url = reverse(
            'checkout_success',
            args=['59D52EBA7553416385A882EE642D7E0Z']
            )
        self.assertEqual(
            url,
            '/checkout/checkout_success/59D52EBA7553416385A882EE642D7E0Z'
            )
