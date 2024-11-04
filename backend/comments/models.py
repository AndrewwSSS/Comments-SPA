import os
import uuid

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify


def unique_file_path(instance, filename):
    ext = filename.split(".")[-1]

    base_filename = slugify(".".join(filename.split(".")[:-1]))

    return f"{base_filename}_{uuid.uuid4().hex}.{ext}"


class Comment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    parent_message = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies"
    )
    created_at = models.DateTimeField(default=timezone.now)
    content = models.TextField()
    image = models.ImageField(blank=True, null=True, upload_to=unique_file_path)
    text_file = models.FileField(blank=True, null=True, upload_to=unique_file_path)

    class Meta:
        ordering = ["-created_at"]
