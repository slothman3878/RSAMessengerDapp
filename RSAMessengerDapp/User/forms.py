from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User, UserManager

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