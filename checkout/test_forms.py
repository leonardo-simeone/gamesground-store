from django.test import TestCase
from .models import Order
from .forms import OrderForm


class TestOrderForm(TestCase):

    """
    We have several test methods covering different
    aspects of the Order form.
    - test_form_initialization: Checks if the form's attributes
    are correctly initialized, including placeholders, classes,
    labels, and the autofocus attribute on the 'full_name' field.
    - test_form_placeholder_required_fields: Tests if the placeholders
    for required fields end with an asterisk (*).
    - test_form_placeholder_optional_fields: if the placeholders for
    optional fields do not end with an asterisk (*).
    - test_form_model: Test that the form is associated with the correct
    model (Order) and includes the correct fields from the model's Meta class.
    """

    # Test the form's initialization and fields' attributes.
    def test_form_initialization(self):

        form = OrderForm()
        placeholders = {
            'full_name': 'Full Name *',
            'email': 'Email Address *',
            'phone_number': 'Phone Number *',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City *',
            'street_address1': 'Street Address 1 *',
            'street_address2': 'Street Address 2',
            'county': 'County, State or Locality',
        }

        # Test placeholders and classes
        for field_name, field in form.fields.items():
            if field_name != 'country':
                self.assertEqual(
                    field.widget.attrs['placeholder'], placeholders[field_name]
                    )
                self.assertEqual(
                    field.widget.attrs['class'], 'stripe-style-input'
                    )

        # Test label is set to False for all fields
        for field in form.fields.values():
            self.assertFalse(field.label)

        # Test autofocus on the 'full_name' field
        self.assertTrue(form.fields['full_name'].widget.attrs['autofocus'])

    # Test placeholders for required fields.
    def test_form_placeholder_required_fields(self):

        form = OrderForm()
        required_fields = [
            'full_name', 'email', 'phone_number',
            'town_or_city', 'street_address1'
            ]

        for field_name in required_fields:
            self.assertTrue(form.fields[field_name].required)
            self.assertTrue(
                form.fields[field_name].widget.attrs['placeholder'].endswith
                ('*')
                )

    # Test placeholders for optional fields.
    def test_form_placeholder_optional_fields(self):

        form = OrderForm()
        optional_fields = ['postcode', 'street_address2', 'county']

        for field_name in optional_fields:
            self.assertFalse(form.fields[field_name].required)
            self.assertFalse(
                form.fields[field_name].widget.attrs['placeholder'].endswith
                ('*')
                )

    # Test if the form is associated with the correct model.
    def test_form_model(self):

        form = OrderForm()
        self.assertEqual(form.Meta.model, Order)
        self.assertEqual(
            form.Meta.fields,
            ('full_name', 'email', 'phone_number',
             'street_address1', 'street_address2',
             'town_or_city', 'postcode', 'country', 'county',)
            )
