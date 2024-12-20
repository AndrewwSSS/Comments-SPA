import sys
from io import BytesIO

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField
from PIL import Image

from comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    text_file = serializers.FileField(required=False)
    user = serializers.StringRelatedField(read_only=True, source="user.username")

    class Meta:
        model = Comment
        fields = [
            "id",
            "content",
            "user",
            "text_file",
            "image",
            "created_at",
            "parent_message",
            "homepage_url"
        ]
        read_only_fields = [
            "created_at",
            "id",
        ]

    @staticmethod
    def validate_image(image):
        if image:
            valid_image_formats = ["image/jpeg", "image/png", "image/gif"]
            if image.content_type not in valid_image_formats:
                raise serializers.ValidationError("Invalid image type. Allowed types: JPG, PNG, GIF.")

            img = Image.open(image)
            max_width = settings.MAX_IMAGE_WIDTH_KB
            max_height = settings.MAX_IMAGE_HEIGHT_KB
            if img.width > max_width or img.height > max_height:
                img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)

                image_buffer = BytesIO()
                img_format = img.format if img.format else 'JPEG'
                img.save(image_buffer, format=img_format)
                image_buffer.seek(0)

                image = InMemoryUploadedFile(
                    image_buffer,
                    None,
                    image.name,
                    image.content_type,
                    sys.getsizeof(image_buffer),
                    None
                )
        return image

    @staticmethod
    def validate_text_file(text_file):
        if text_file:
            if text_file.content_type != "text/plain":
                raise serializers.ValidationError("Invalid format type")

            max_file_size_kb = 100
            if text_file.size > max_file_size_kb * 1024:
                raise serializers.ValidationError(f"Max file size: {max_file_size_kb} КБ.")

        return text_file


class ListCommentSerializer(CommentSerializer):
    replies_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "content",
            "user",
            "text_file",
            "image",
            "created_at",
            "parent_message",
            "replies_count",
            "homepage_url"
        ]
        read_only_fields = [
            "created_at",
            "id",
            "replies_count",
        ]


class CreateCommentSerializer(CommentSerializer):
    def create(self, validated_data):
        return Comment.objects.create(
            **validated_data,
            user=self.context["request"].user
        )
