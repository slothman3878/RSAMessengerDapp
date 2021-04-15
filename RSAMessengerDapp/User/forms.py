from django import forms
from django.contrib.auth.forms import UserCreationForm

from Crypto.PublicKey import RSA

from .models import User, UserManager, Key

class SignupForm(UserCreationForm): 
    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password1'],
        )
        return user

    class Meta:
        model = User
        fields = ("username","password1","password2")

class KeyGenerationForm(forms.Form):
    passphrase = forms.CharField(max_length=120, required=False, help_text='passphrase should be at most 120 characters long')