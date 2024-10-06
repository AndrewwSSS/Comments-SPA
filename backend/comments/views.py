from asgiref.sync import async_to_sync
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from channels.layers import get_channel_layer

from .models import Comment
from .serializers import CommentSerializer


class CommentViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin
):
    queryset = Comment.objects.filter(parent_message__isnull=True)
    ordering_fields = ["created_at", "user__username", "user__email"]
    serializer_class = CommentSerializer

    @method_decorator(cache_page(60 * 5, key_prefix="comments_list"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "chat_room",
            {
                "type": "chat_message",
                "comment": serializer.data
            }
        )

        return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
            )
