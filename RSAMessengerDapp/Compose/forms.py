from django import forms

# Need to write validation methods
class MessageComposeForm(forms.Form):
    title = forms.CharField(max_length=280, required=True, help_text='280 characters or less')
    body = forms.CharField(widget=forms.Textarea, help_text='Write in html syntax')
    recipient = forms.CharField(max_length=42, required=True, help_text='Use a Valid ethereum address')

    def clean_recipient(self, *args, **kwargs):
        recipient = self.cleaned_data.get('recipient')
        if recipient[:2]=='0x' and len(recipient)==42:
            return recipient
        else:
            raise forms.ValidationError('Invalid Ethereum Address')

    def clean_title(self, *args, **kwargs):
        title = self.cleaned_data.get('title')
        if len(title)>280:
            raise forms.ValidationError('Title too long (must be 280 characters or less')
        else:
            return title