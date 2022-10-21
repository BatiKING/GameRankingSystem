from django import forms
from django.contrib.auth.forms import UserCreationForm
from Game_Ranking_System.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput())


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.', required=True)
    nickname = forms.CharField(max_length=150, help_text='Your Nickname is what others see', required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'nickname', 'password1', 'password2',)
