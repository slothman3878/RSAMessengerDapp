from django import forms

class KeyGenerationForm(forms.Form):
    #The passphrase character limit is tbh unnecessary. 120 character limit is more for convenience than anything
    passphrase = forms.CharField(max_length=120, required=False, help_text='passphrase is ideally at most 120 characters long')