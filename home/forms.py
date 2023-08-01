from django import forms
from .models import Contact, Newsletter


class ContactForm(forms.ModelForm):

    """
    A form to render the fields to use in the contact form.
    """

    class Meta:
        model = Contact
        fields = ['name', 'email', 'body']

    def __init__(self, *args, **kwargs):
        """
        Add placeholders, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'name': 'Full Name',
            'email': 'E-mail address',
            'body': 'Write your message here',
        }

        for field in self.fields:

            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder

        self.fields[field].label = False
        self.fields['name'].widget.attrs['autofocus'] = True


class NewsletterForm(forms.ModelForm):

    """
    A form to render the fields to use in the newsletter form.
    """

    class Meta:
        model = Newsletter
        fields = ['name', 'email']

    def __init__(self, *args, **kwargs):
        """
        Add placeholders, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'name': 'Name',
            'email': 'E-mail address',
        }

        for field in self.fields:

            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder

        self.fields[field].label = False
        self.fields['name'].widget.attrs['autofocus'] = True
