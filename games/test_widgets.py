import unittest
from django.forms.widgets import ClearableFileInput
from django.utils.translation import gettext_lazy as _
from django.test import SimpleTestCase
from django.forms import Form
from .widgets import CustomClearableFileInput


class TestCustomClearableFileInput(unittest.TestCase):

    """
    We have several test methods covering different aspects of
    the CustomClearableFileInput class.
    - test_clear_checkbox_label: Tests that the clear checkbox
    label is 'Remove'.
    - test_initial_text: Tests that the initial test is 'Current Image'.
    - test_input_text: Tests that the input text is an empty string.
    - test_template_name: Tests that the correct template is used.
    """

    def test_clear_checkbox_label(self):
        widget = CustomClearableFileInput()
        self.assertEqual(widget.clear_checkbox_label, _('Remove'))

    def test_initial_text(self):
        widget = CustomClearableFileInput()
        self.assertEqual(widget.initial_text, _('Current Image'))

    def test_input_text(self):
        widget = CustomClearableFileInput()
        self.assertEqual(widget.input_text, _(''))

    def test_template_name(self):
        widget = CustomClearableFileInput()
        self.assertEqual(
            widget.template_name,
            'games/custom_widget_templates/custom_clearable_file_input.html'
            )
