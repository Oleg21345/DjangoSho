from django.shortcuts import render, redirect
from shop.forms import LoginForm, RegisterForm
from django.contrib.auth import login, logout
from django.contrib import messages


def login_registration(requests):
    context = {
        "title": "Увійти або зареєструватися",
        "login_form": LoginForm,
        "register_form": RegisterForm
    }
    return render(requests,"shop/login_or_reg.html", context)


def user_login(requests):
    form = LoginForm(data=requests.POST)
    if form.is_valid():
        user = form.get_user()
        login(requests, user)
        messages.success(requests, "Ви успішно увійшли")
        return redirect("home")
    else:
        messages.error(requests, "Не правельне ім'я або пароль")
        return redirect("login_register")


def user_logout(requests):
    logout(requests)
    return redirect("home")


def register_user(requests):
    form = RegisterForm(data=requests.POST)
    if form.is_valid():
        form.save()
        messages.success(requests, "Ви успішно зареєстрували новий акаунт")
    else:
        for error in form.errors:
            messages.error(requests, form.errors[error].as_text())
    return redirect("login_register")

