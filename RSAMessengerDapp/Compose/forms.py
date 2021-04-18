from django import forms

class MessageComposeForm(forms.Form):
    title = forms.CharField(max_length=280, required=True, help_text='280 characters or less')
    body = forms.CharField(widget=forms.Textarea)
    recipient = forms.CharField(max_length=42, required=True)