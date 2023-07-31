from django import forms
from .widgets import CustomClearableFileInput
from .models import *


class GameForm(forms.ModelForm):

    class Meta:
        model = Game
        exclude = ('likes',)

    image = forms.ImageField(label='Image', required=False, widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        platforms = Platform.objects.all()
        names = [(p.id, p.name) for p in platforms]

        self.fields['platform'].choices = names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded'

        pegi_ratings = Pegi.objects.all()
        ages = [(pr.id, pr.age) for pr in pegi_ratings]

        self.fields['pegi_rating'].choices = ages
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded'

        self.fields['name'].widget.attrs['autofocus'] = True
