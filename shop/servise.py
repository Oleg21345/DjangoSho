from django.core.mail import send_mail
from conf import settings


def send(user_mail):
    send_mail(
        subject="У нас нова пропозиція",
        message="Підписуйся",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_mail],
        fail_silently=False,
    )