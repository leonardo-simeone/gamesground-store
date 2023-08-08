import unittest
from django.test import TestCase
from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress
from django.forms import ModelForm
from .models import UserProfile
from .forms import *


class TestUserProfileForm(unittest.TestCase):

    """
    The setUp method is used to create user_profile data.
    We have several test methods covering different
    aspects of the UserProfileForm.
    - test_user_profile_form_valid: Tests that the user_profile data
    is valid when UserProfileForm is populated with it.
    - test_user_profile_form_required_fields: Tests that even with empty
    fields the form is still valid since no field is required.
    - test_user_profile_form_autofocus: Tests that default_phone_number
    is in fact autofocused.
    - test_user_profile_form_placeholder: Tests that the form's placeholders
    are all as expected.
    - test_user_profile_form_css_class: Tests that the classes added
    to the fields are as expected.
    - test_user_profile_form_labels: Test that the labels are removed
    from the fields.
    """

    def setUp(self):
        self.user_profile_data = {
            'default_phone_number': '1234567890',
            'default_postcode': '12345',
            'default_town_or_city': 'Test City',
            'default_street_address1': 'Test Street 1',
            'default_street_address2': 'Test Street 2',
            'default_county': 'Test County',
        }

    # Test form is valid with user_profile_data
    def test_user_profile_form_valid(self):
        form = UserProfileForm(data=self.user_profile_data)
        self.assertTrue(form.is_valid())

    # Test no field is required
    def test_user_profile_form_required_fields(self):
        required_fields = [
            'default_phone_number',
            'default_postcode',
            'default_town_or_city',
            'default_street_address1',
        ]

        for field_name in required_fields:
            data = self.user_profile_data.copy()
            del data[field_name]
            form = UserProfileForm(data=data)
            self.assertTrue(form.is_valid())

    # Test correct field is autofocused
    def test_user_profile_form_autofocus(self):
        form = UserProfileForm()
        self.assertTrue(
            form.fields['default_phone_number'].widget.attrs.get('autofocus')
            )

    # Test correct placeholders are used
    def test_user_profile_form_placeholder(self):
        form = UserProfileForm()
        placeholders = {
            'default_phone_number': 'Phone Number',
            'default_postcode': 'Postal Code',
            'default_town_or_city': 'Town or City',
            'default_street_address1': 'Street Address 1',
            'default_street_address2': 'Street Address 2',
            'default_county': 'County, State or Locality',
        }

        for field_name, placeholder in placeholders.items():
            self.assertEqual(
                form.fields[field_name].widget.attrs.get('placeholder'),
                placeholder
                )

    # Test that correct classes are added
    def test_user_profile_form_css_class(self):
        form = UserProfileForm()
        css_class = 'border-black rounded profile-form-input'

        for field_name in form.fields:
            self.assertEqual(
                form.fields[field_name].widget.attrs.get('class'), css_class
                )

    # Test that labels are removed
    def test_user_profile_form_labels(self):
        form = UserProfileForm()

        for field_name in form.fields:
            self.assertFalse(form.fields[field_name].label)


User = get_user_model()


class TestCustomSignupForm(TestCase):

    """
    The setUp method is used to create user_profile data.
    We have several test methods covering different
    aspects of the CustomSignupForm.
    - test_signup_form_save: Tests that the form_data
    is valid that the CustomSignupForm is saved, that the attributes
    are correct but the email_address is not verified because
    a confirmation from the user via email has to happen first.
    - test_signup_form_invalid: Tests that the CustomSignupForm
    is invalid when invalid fields.
    - test_signup_form_missing_fields: Tests that the CustomSignupForm
    is invalid when missing fields.
    - test_signup_form_placeholders: Tests that the form's placeholders
    are all as expected.
    - test_signup_form_autofocus: Tests that first_name is
    in fact autofocused.
    """

    def test_signup_form_save(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'john@example.com',
            'email2': 'john@example.com',
            'password1': 'securepassword',
            'password2': 'securepassword',
        }
        form = CustomSignupForm(data=form_data)
        self.assertTrue(form.is_valid())

        user = form.save(self.request)

        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.email, 'john@example.com')

        # Check if the email address is verified
        email_address = EmailAddress.objects.get(user=user)
        self.assertFalse(email_address.verified)

    def setUp(self):
        self.request = self.client.request().wsgi_request

    def test_signup_form_invalid(self):
        # Test when the form data is invalid
        form_data = {
            'first_name': 'John',
            'last_name': '',  # Invalid, last name is required
            'username': 'johndoe',
            'email': 'invalidemail',  # Invalid email format
            'email2': 'john@example.com',
            'password1': 'securepassword',
            'password2': 'differentpassword',  # Passwords don't match
        }
        form = CustomSignupForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_signup_form_missing_fields(self):
        # Test when required fields are missing
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'password1': 'securepassword',
            'password2': 'securepassword',
        }
        form = CustomSignupForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_signup_form_placeholders(self):
        placeholders = {
            'first_name': 'First Name *',
            'last_name': 'Last Name *',
            'username': 'Username *',
            'email': 'E-mail address *',
            'email2': 'E-mail address confirmation *',
            'password1': 'Password *',
            'password2': 'Password (again) *',
        }
        form = CustomSignupForm()

        for field_name, expected_placeholder in placeholders.items():
            field = form.fields[field_name]
            self.assertEqual(
                field.widget.attrs.get('placeholder'), expected_placeholder
                )

    def test_signup_form_autofocus(self):
        form = CustomSignupForm()

        self.assertEqual(
            form.fields['username'].widget.attrs.get('autofocus'), False
            )
        self.assertEqual(
            form.fields['first_name'].widget.attrs.get('autofocus'), True
            )
