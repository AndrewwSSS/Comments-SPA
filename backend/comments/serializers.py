from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from .models import Comment


class ListCommentSerializer(serializers.ModelSerializer):
    replies = serializers.ListSerializer(
        child=RecursiveField(),
        required=False,
    )

    class Meta:
        model = Comment
        fields = [
            "id",
            "content",
            "replies",
            "user"
        ]


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "content",
            "parent_message"
        ]

    def create(self, validated_data):
        return Comment.objects.create(
            **validated_data,
            user=self.context["request"].user
        )
