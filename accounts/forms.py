#Edwin domale 
# Azim Shahul Hameed
#Ernesto Cosentino
# Nayim Amdouni
# Muhammad Ozair Khan
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model as user_model
from django.contrib.auth.forms import PasswordChangeForm
from django import forms

User = user_model()

class UserRegistrationForm(UserCreationForm):
    firstname = forms.CharField(max_length=30)
    lastname = forms.CharField(max_length=30)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['firstname', 'lastname', 'email', 'password1', 'password2']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'firstname','lastname', 'phone']

USER_ROLES = (
    ('user', 'User'),   # Normal user
    ('admin', 'Admin')  # Superuser aka admin
)
