from django.test import TestCase
from .forms import *


class TestContactForm(TestCase):

    """
    We have four test methods: test_form_required_fields,
    test_form_placeholders, test_form_label_visibility,
    and test_form_autofocus.
    - In test_form_required_fields, we check if the form fields
    match the expected required field names.
    - In test_form_placeholders, we test if the placeholders for each
    form field match the expected values.
    - In test_form_label_visibility, we verify that the labels for
    all fields are set to False.
    - In test_form_autofocus, we test if the autofocus attribute is set
    for the "name" field.
    """

    def test_form_required_fields(self):
        form = ContactForm()
        self.assertTrue(form.fields['name'].required)
        self.assertTrue(form.fields['email'].required)
        self.assertTrue(form.fields['body'].required)

    def test_form_placeholders(self):
        form = ContactForm()
        self.assertEqual(
            form.fields['name'].widget.attrs['placeholder'], 'Full Name *'
            )
        self.assertEqual(
            form.fields['email'].widget.attrs['placeholder'],
            'E-mail address *'
            )
        self.assertEqual(
            form.fields['body'].widget.attrs['placeholder'],
            'Write your message here *'
            )

        placeholders = {
            'name': 'Full Name *',
            'email': 'E-mail address *',
            'body': 'Write your message here *',
        }

        for field_name, placeholder_text in placeholders.items():
            self.assertEqual(
                form.fields[field_name].widget.attrs['placeholder'],
                placeholder_text
                )

    def test_form_label_visibility(self):
        form = ContactForm()
        self.assertFalse(form.fields['name'].label)
        self.assertFalse(form.fields['email'].label)
        self.assertFalse(form.fields['body'].label)

    def test_form_autofocus(self):
        form = ContactForm()
        self.assertTrue(form.fields['name'].widget.attrs.get('autofocus'))
        self.assertIsNone(form.fields['email'].widget.attrs.get('autofocus'))
        self.assertIsNone(form.fields['body'].widget.attrs.get('autofocus'))


class TestNewsletterForm(TestCase):

    """
    We have four test methods: test_form_required_fields,
    test_form_placeholders, test_form_label_visibility,
    and test_form_autofocus.
    - In test_form_required_fields, we check if the form fields
    match the expected required field names.
    - In test_form_placeholders, we test if the placeholders for each
    form field match the expected values.
    - In test_form_label_visibility, we verify that the labels for
    all fields are set to False.
    - In test_form_autofocus, we test if the autofocus attribute is set
    for the "name" field.
    """

    def test_form_required_fields(self):
        form = NewsletterForm()
        self.assertTrue(form.fields['name'].required)
        self.assertTrue(form.fields['email'].required)

    def test_form_placeholders(self):
        form = NewsletterForm()
        self.assertEqual(
            form.fields['name'].widget.attrs['placeholder'], 'Name *'
            )
        self.assertEqual(
            form.fields['email'].widget.attrs['placeholder'],
            'E-mail address *'
            )

        placeholders = {
            'name': 'Name *',
            'email': 'E-mail address *',
        }

        for field_name, placeholder_text in placeholders.items():
            self.assertEqual(
                form.fields[field_name].widget.attrs['placeholder'],
                placeholder_text
                )

    def test_form_label_visibility(self):
        form = NewsletterForm()
        self.assertFalse(form.fields['name'].label)
        self.assertFalse(form.fields['email'].label)

    def test_form_autofocus(self):
        form = NewsletterForm()
        self.assertTrue(form.fields['name'].widget.attrs.get('autofocus'))
        self.assertIsNone(form.fields['email'].widget.attrs.get('autofocus'))
