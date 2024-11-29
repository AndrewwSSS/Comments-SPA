import pika
from django.conf import settings
from pika.adapters.blocking_connection import BlockingChannel


class RabbitMQProducer:
    channel: BlockingChannel = None

    def __init__(self):
        if not RabbitMQProducer.channel:
            RabbitMQProducer.init_producer()

        self.channel = RabbitMQProducer.channel

    def publish_user_acc_activation(self, body: str) -> None:
        self.channel.basic_publish(
            exchange="",
            routing_key="user-account-activation",
            body=body,
        )

    def publish_new_active_user(self, body: str) -> None:
        self.channel.basic_publish(
            exchange="",
            routing_key="new-active-user",
            body=body,
        )

    @classmethod
    def init_producer(cls):
        if cls.channel:
            return

        credentials = pika.PlainCredentials(
            settings.RABBITMQ_USER,
            settings.RABBITMQ_PASSWORD
        )
        connection_params = pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            credentials=credentials
        )
        connection = pika.BlockingConnection(connection_params)
        cls.channel = connection.channel()
        cls.channel.queue_declare(queue="new-active-user", durable=True)
        cls.channel.queue_declare(queue="user-account-activation", durable=True)
