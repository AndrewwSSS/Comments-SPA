from django.core.management import BaseCommand

from pubsub.sub import NewUserSubscriber


class Command(BaseCommand):
    def handle(self, *args, **options):
        subscriber = NewUserSubscriber()
        subscriber.start()
