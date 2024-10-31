from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from user.models import User


@shared_task
def send_welcome_email(user_id: int):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        print(f"User with id {user_id} does not exist.")
        return
        
    subject = "Welcome to Our Platform!"
    message = render_to_string("emails/welcome_email.html", {"user": user})

    send_mail(
        subject,
        "",
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=message
    )

    print(f"Welcome email sent to {user.email}")


