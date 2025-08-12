from shop.models import  Gmail
from django.contrib import messages
from django.shortcuts import redirect, render


def add_subs_gmail(request):
    """Додавання пошти для підписання на розсилки"""
    gmail = request.POST.get("gmail")
    user = request.user if request.user.is_authenticated else None
    if gmail:
        try:
            Gmail.objects.create(gmail=gmail, user=user)
        except Exception as err:
            print(f"Error is {err}")
            messages.error(request, "Така пошта вже зареєстрована")

    return redirect("home")


def send_email_to_subs(request):
    """Відправка імейлу до користувача"""
    from conf import settings
    from django.core.mail import send_mail
    if request.method == "POST":
        text = request.POST.get("text")
        mail_lists = Gmail.objects.all()
        for mail in mail_lists:
            send_mail(
                subject="У нас нова пропозиція",
                message=text,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[mail.gmail],
                fail_silently=False,
            )
            print(f"Повідомлення відправлене на пошту {mail} ----- {bool(send_mail)}")

    context = {
        "title": "Спам ліст"
    }
    return render(request, "shop/send_gmail.html", context)
