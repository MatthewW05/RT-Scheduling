from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    initials = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "initials", "username", "password1", "password2"]