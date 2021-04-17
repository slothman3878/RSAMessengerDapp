from django import forms

class KeyGenerationForm(forms.Form):
    passphrase = forms.CharField(max_length=120, required=False, help_text='passphrase should be at most 120 characters long')