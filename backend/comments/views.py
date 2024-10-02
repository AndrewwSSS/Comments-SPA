from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets, mixins

from .models import Comment
from .serializers import ListCommentSerializer
from .serializers import CreateCommentSerializer


class CommentViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin
):
    queryset = Comment.objects.filter(parent_message__isnull=True)
    ordering_fields = ["created_at", "user__username", "user__email"]

    def get_serializer_class(self):
        if self.action == "create":
            return CreateCommentSerializer
        return ListCommentSerializer

    @method_decorator(cache_page(60 * 5, key_prefix="comments_list"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
