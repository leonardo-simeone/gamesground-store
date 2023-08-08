import unittest
from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile


class TestUserProfileModel(TestCase):

    """
    The setUp method is used to create a User object and the get the
    UserProfile related to it.
    We have two test methods: test_user_profile_creation and
    test_signal_bypass.
    - In test_user_profile_creation, we test that the user profile
    has been created right after creating the user and that the profile
    fields are all None except for username.
    - In test_signal_bypass, we populate the user profile, save it
    bypassing the signal and assertEqual that all the fields match,
    which is the equivalent to updating the user profile.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword"
        )
        self.profile = UserProfile.objects.get(user=self.user)

    def test_user_profile_creation(self):
        # Verify the user profile has been created
        self.assertEqual(self.user.username, str(self.profile))
        self.assertIsNone(self.profile.default_phone_number)
        self.assertIsNone(self.profile.default_street_address1)
        self.assertIsNone(self.profile.default_street_address2)
        self.assertIsNone(self.profile.default_town_or_city)
        self.assertIsNone(self.profile.default_county)
        self.assertIsNone(self.profile.default_postcode)
        self.assertEqual(self.profile.default_country, None)

    def test_signal_bypass(self):
        # Save the profile without using the signal
        self.profile.default_phone_number = '123456789'
        self.profile.default_street_address1 = '123 Main St'
        self.profile.default_street_address2 = 'Apt 4B'
        self.profile.default_town_or_city = 'Cityville'
        self.profile.default_county = 'Countyshire'
        self.profile.default_postcode = '12345'
        self.profile.default_country = 'Ireland'
        self.profile.save(using=self.profile._state.db)

        # Test that all fields just saved match
        updated_profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(updated_profile.default_phone_number, '123456789')
        self.assertEqual(
            updated_profile.default_street_address1,
            '123 Main St'
            )
        self.assertEqual(updated_profile.default_street_address2, 'Apt 4B')
        self.assertEqual(updated_profile.default_town_or_city, 'Cityville')
        self.assertEqual(updated_profile.default_county, 'Countyshire')
        self.assertEqual(updated_profile.default_postcode, '12345')
        self.assertEqual(updated_profile.default_country, 'Ireland')
