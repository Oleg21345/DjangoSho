from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, User
from shop.models import Reviews, Customer, ShippingAddress


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


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ("text", "rating")

        widgets = {
            "text": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Додати відгук",
                "rows": 3
            }),
            'rating': forms.HiddenInput()
        }


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ("first_name", "last_name", "gmail", "phone_number")
        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Тарас"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Шевченко"}
            ),
            "gmail": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "tarasshevchenko@gmail.com"}
            ),
            "phone_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "380999999999"}
            ),
        }




class ShippingForm(forms.ModelForm):

    class Meta:
        model = ShippingAddress
        fields = ("city", "state", "street")
        widgets = {
            "city": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Львів"}
            ),
            "state": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Личаківський"}
            ),
            "street": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Багалія"}
            ),
        }












