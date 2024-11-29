import json

import pika
import threading

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from user.models import User


class NewUserSubscriber(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        credentials = pika.PlainCredentials(
            settings.RABBITMQ_USER,
            settings.RABBITMQ_PASSWORD
        )
        connection_params = pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            credentials=credentials
        )
        self.connection = pika.BlockingConnection(connection_params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue="new-active-user", durable=True)
        self.channel.queue_declare(queue="user-account-activation", durable=True)
        self.channel.basic_consume(
            queue="user-account-activation",
            on_message_callback=self._user_account_activation
        )
        self.channel.basic_consume(
            queue="new-active-user",
            on_message_callback=self._new_active_user
        )

    @staticmethod
    def _user_account_activation(ch, method, properties, body):
        payload = json.loads(body.decode("utf-8"))
        user_id = payload["id"]
        token = payload["token"]

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            print(f"User with id {user_id} does not exist.")
            return

        subject = "Account verification"
        message = render_to_string(
            "emails/verification_email.html",
            {"user": user, "token": token}
        )

        send_mail(
            subject,
            "",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=message
        )

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def _new_active_user(self, ch, method, properties, body):
        payload = json.loads(body.decode("utf-8"))
        user_id = payload["id"]

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
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def run(self):
        self.channel.start_consuming()
