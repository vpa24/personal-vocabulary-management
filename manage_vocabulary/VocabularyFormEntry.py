from django import forms
from .models import WordEntry


class VocabularyFormEntry(forms.Form):
    class Meta:
        model = WordEntry
        fields = ['word_type', 'definition', 'example']

    example = forms.CharField(
        label="Example:",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '2', "placeholder": "You can add one or more example sentences"}))

    part_of_speech = forms.ChoiceField(
        label="Part of speech:",
        choices=[("-", "-------------")] + WordEntry.WORD_TYPES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    definition = forms.CharField(
        label="Definition:",
        widget=forms.TextInput(
            attrs={'class': "form-control", 'autocompelte': 'off', "placeholder": "Please Enter Description"}),
        required=True
    )
