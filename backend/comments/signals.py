from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from .models import Comment


def invalidate_cache_by_pattern(pattern: str) -> None:
    cache.delete_pattern(pattern)


@receiver(post_save, sender=Comment)
def invalidate_comments_list_on_save(sender, instance, **kwargs):
    invalidate_cache_by_pattern("*.comments_list.*")


@receiver(post_delete, sender=Comment)
def invalidate_comments_list_on_delete(sender, instance, **kwargs):
    invalidate_cache_by_pattern("*.comments_list.*")
