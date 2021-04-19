from django import forms

# Need to write validation methods
class MessageComposeForm(forms.Form):
    title = forms.CharField(max_length=280, required=True, help_text='280 characters or less')
    body = forms.CharField(widget=forms.Textarea, help_text='Write in html format')
    recipient = forms.CharField(max_length=42, required=True, help_text='Use a Valid ethereum address')