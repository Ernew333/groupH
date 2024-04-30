from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model as user_model
from django.contrib.auth.forms import PasswordChangeForm
from django import forms

User = user_model()

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

