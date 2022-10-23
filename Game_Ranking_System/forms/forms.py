from django import forms
from django.contrib.auth.forms import UserCreationForm
from Game_Ranking_System.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}), )


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.',
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.',
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.', required=True,
                             widget=forms.TextInput(attrs={"class": "form-control"}))
    nickname = forms.CharField(max_length=150, help_text='Your Nickname is what others see', required=True,
                               widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'nickname', 'password1', 'password2',)
        widgets = {'username': forms.TextInput(attrs={"class": "form-control"}),
                   'first_name': forms.TextInput(attrs={"class": "form-control"}),
                   'last_name': forms.TextInput(attrs={"class": "form-control"}),
                   'email': forms.TextInput(attrs={"class": "form-control"}),
                   'nickname': forms.TextInput(attrs={"class": "form-control"}),
                   'password1': forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
                   'password2': forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'})}
