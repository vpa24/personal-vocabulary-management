from django import forms
from .models import WordEntry

class VocabularyForm(forms.Form):
    name = forms.CharField( 
        label="Name:",
        widget=forms.TextInput(
            attrs={'class': "form-control w-md-50 w-sm-100", 'autocomplete': 'off',"placeholder": "Please enter a vocabulary name"}),
        required=True 
    )