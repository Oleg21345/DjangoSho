from shop.models import  Gmail
from django.contrib import messages
from django.shortcuts import redirect, render
from shop.tasks import send_msg_to_email, send_email_to_subs_task


def add_subs_gmail(request):
    """Додавання пошти для підписання на розсилки"""
    gmail = request.POST.get("gmail")
    user = request.user if request.user.is_authenticated else None
    if gmail:
        try:
            Gmail.objects.create(gmail=gmail, user=user)
            send_msg_to_email.delay(gmail)
        except Exception as err:
            print(f"Error is {err}")
            messages.error(request, "Така пошта вже зареєстрована")

    return redirect("home")


def send_email_to_subs(request):
    if request.method == "POST":
        text = request.POST.get("text")
        send_email_to_subs_task.delay(text, schedule=0)

    context = {"title": "Спам ліст"}
    return render(request, "shop/send_gmail.html", context)