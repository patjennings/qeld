from django import forms
from .models import Game

class AuthForm(forms.Form):
    password = forms.CharField(label="password", max_length=256)
