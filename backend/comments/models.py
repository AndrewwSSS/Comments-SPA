import os
import uuid

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify


def unique_file_path(instance, filename):
    ext = filename.split(".")[-1]

    base_filename = slugify(".".join(filename.split(".")[:-1]))
    unique_filename = f"{base_filename}_{uuid.uuid4().hex}.{ext}"

    directory = "comments/files"

    return os.path.join(directory, unique_filename)


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
    image = models.ImageField(upload_to=unique_file_path, blank=True, null=True)
    text_file = models.FileField(upload_to=unique_file_path, blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]
    