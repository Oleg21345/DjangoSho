from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, User



class LoginForm(AuthenticationForm):

    username = forms.CharField(
        label="Ім'я користувача",
        max_length=80,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Ім'я користувача"
        })
    )

    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Пароль"
        })
    )


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2"
        )

    username = forms.CharField(
        label="Ім'я користувача",
        max_length=80,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Ім'я користувача"
        })
    )

    email = forms.EmailField(
        label="Пошта",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Електрона пошта"
        })
    )

    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Пароль"
        })
    )

    password2 = forms.CharField(
        label="Повторний пароль",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Повторити пароль"
        })
    )