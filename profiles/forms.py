from allauth.account.forms import SignupForm
from django import forms
from .models import UserProfile


class CustomSignupForm(SignupForm):
    """
    A class to customize the django predetermined
    signup form by adding first and last names to it
    """

    first_name = forms.CharField(max_length=50, label='First Name')
    last_name = forms.CharField(max_length=50, label='Last Name')

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user

    class Meta:
        model = SignupForm
        fields = ('first_name', 'last_name', 'username',
                  'email', 'email2',
                  'password1', 'password2',)

    field_order = [
        'first_name', 'last_name', 'username', 'email',
        'email2', 'password1', 'password2',
        ]

    def __init__(self, *args, **kwargs):
        """
        Add placeholders, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'username': 'Username',
            'email': 'E-mail address',
            'email2': 'E-mail address confirmation',
            'password1': 'Password',
            'password2': 'Password (again)',
        }

        self.fields['username'].widget.attrs['autofocus'] = False
        self.fields['first_name'].widget.attrs['autofocus'] = True
        for field in self.fields:

            placeholder = f'{placeholders[field]} *'
            self.fields[field].widget.attrs['placeholder'] = placeholder

        self.fields[field].label = False


class UserProfileForm(forms.ModelForm):
    """
    A class to create the user profile form. It has
    a meta class to determine the fields, and a helper
    method to loop through the fields to add placeholders,
    add classes and set autofocus
    """

    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'default_phone_number': 'Phone Number',
            'default_postcode': 'Postal Code',
            'default_town_or_city': 'Town or City',
            'default_street_address1': 'Street Address 1',
            'default_street_address2': 'Street Address 2',
            'default_county': 'County, State or Locality',
        }

        self.fields['default_phone_number'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'default_country':

                placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder

            self.fields[field].widget.attrs['class'] = (
                'border-black rounded profile-form-input'
                )
            self.fields[field].label = False
