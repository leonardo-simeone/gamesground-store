from django.test import SimpleTestCase
from django.urls import reverse, resolve
from .views import profile, order_history


class TestProfilesUrls(SimpleTestCase):

    """
    Both methods test that the urls gotten for each view are correct.
    """

    def test_profile_url_resolves(self):
        url = reverse('profile')
        self.assertEqual(resolve(url).func, profile)

    def test_order_history_url_resolves(self):
        url = reverse(
            'order_history', args=['59D52EBA7553416385A882EE642D7E0Z']
            )
        self.assertEqual(resolve(url).func, order_history)
