from celery import shared_task
from user.models import User


@shared_task
def send_welcome_email(user: User):
    ...
