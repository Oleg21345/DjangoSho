from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, User
from shop.models import Reviews, Customer, ShippingAddress, Product, Category, Galery
from django.utils.translation import gettext as _
from django.forms import inlineformset_factory


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label=_("Ім'я користувача"),
        max_length=80,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": _("Ім'я користувача")
        })
    )

    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": _("Пароль")
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
        label=_("Ім'я користувача"),
        max_length=80,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": _("Ім'я користувача")
        })
    )

    email = forms.EmailField(
        label=_("Пошта"),
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": _("Електрона пошта")
        })
    )

    password1 = forms.CharField(
        label=_("Пароль"),
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": _("Пароль")
        })
    )

    password2 = forms.CharField(
        label=_("Повторний пароль"),
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": _("Повторити пароль")
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


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title', 'img', 'parent', 'slug']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Назва категорії'}),
            'img': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'parent': forms.Select(attrs={'class': 'form-select'}),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Slug (не редагується)',
                'readonly': True}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "title",
            "price",
            "quantity",
            "desc",
            "info",
            "category",
            "size",
            "color",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Назва продукту"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
            "desc": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "info": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "size": forms.NumberInput(attrs={"class": "form-control"}),
            "color": forms.TextInput(attrs={"class": "form-control"}),
        }

class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class GaleryForm(forms.ModelForm):
    class Meta:
        model = Galery
        fields = ["img"]
        widgets = {
            "img": MultiFileInput(attrs={"class": "form-control", "multiple": True}),
        }

GaleryFormSet = inlineformset_factory(
    Product, Galery,
    fields=('img',),
    extra=3,
    can_delete=True
)









