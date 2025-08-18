from conf.celery import background_task
from shop.servise import send
from shop.models import Gmail
from conf import settings
from django.core.mail import send_mail
from celery import shared_task


@background_task.task
def send_msg_to_email(user_email):
    send(user_email)


@background_task.task
def send_spam():
    user = Gmail.objects.all()
    for users in user:
        send_mail(
            subject="У нас нова пропозиція ми тобі будемо спамити до кінця життя лошок",
            message="Ха-ха лошара ща спамить тобі будемо",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[users.gmail],
            fail_silently=False,
        )


@background_task.task
def send_email_to_subs_task(text, schedule):
    """Фонова розсилка імейлів"""
    mail_lists = Gmail.objects.all()
    for mail in mail_lists:
        send_mail(
            subject="У нас нова пропозиція",
            message=text,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[mail.gmail],
            fail_silently=False,
        )
        print(f"Повідомлення відправлене на пошту {mail.gmail}")