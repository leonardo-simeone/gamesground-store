from django import forms
from .widgets import CustomClearableFileInput
from .models import *


class GameForm(forms.ModelForm):
    """
    A class to create the game objects form. It has
    a meta class to determine the fields, and a helper
    method to loop through the ones with multiple choices,
    add classes to fields and set autofocus
    """

    class Meta:
        model = Game
        exclude = ('likes',)

    image = forms.ImageField(
        label='Image', required=False, widget=CustomClearableFileInput
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        platforms = Platform.objects.all()
        platform_names = [(p.id, p.name) for p in platforms]

        self.fields['platform'].choices = platform_names

        pegi_ratings = Pegi.objects.all()
        pegi_ages = [(pr.id, pr.age) for pr in pegi_ratings]

        self.fields['pegi_rating'].choices = pegi_ages

        # Remove the genre field from the loop
        # that adds classes to other fields
        for field_name, field in self.fields.items():
            if field_name != 'genre':
                # Check if the field is not the image field
                if field_name != 'image':
                    field.widget.attrs['class'] = 'border-black rounded'

        self.fields['name'].widget.attrs['autofocus'] = True
