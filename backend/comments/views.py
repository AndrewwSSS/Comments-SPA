from asgiref.sync import async_to_sync
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from channels.layers import get_channel_layer
from django.core.cache import cache
from django.conf import settings

from comments.models import Comment
from comments.serializers import (
    ListCommentSerializer,
    CreateCommentSerializer,
    CommentSerializer
)


class ReplyPagination(PageNumberPagination):
    page_size = settings.REPLIES_PAGE_SIZE
    page_size_query_param = 'page_size'


class CommentViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin
):
    queryset = Comment.objects.filter(
        parent_message__isnull=True
    ).select_related("user").annotate(
        replies_count=Count("replies")
    ).order_by("-created_at")
    ordering_fields = ["created_at", "user__username", "user__email"]

    def get_serializer_class(self):
        if self.action == "list":
            return ListCommentSerializer
        elif self.action == "create":
            return CreateCommentSerializer
        else:
            return CommentSerializer

    @method_decorator(cache_page(settings.CACHE_TTL, key_prefix="comments_list"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        captcha_key = request.data.get("captcha_key")
        captcha_input = request.data.get("captcha_input", "")

        if not captcha_key:
            return Response(
                {"message": "Captcha key not provided."},
                status=status.HTTP_400_BAD_REQUEST
            )

        captcha_text = cache.get(captcha_key)

        if not captcha_text:
            return Response(
                {"message": "Captcha has expired or not found."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if captcha_text.lower() != captcha_input.lower():
            return Response(
                {"message": "Invalid captcha input."},
                status=status.HTTP_400_BAD_REQUEST
            )

        cache.delete(captcha_key)

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

    @action(detail=True, methods=["get"], url_path="replies")
    def replies(self, request, pk=None):
        replies_qs = Comment.objects.filter(parent_message=pk).select_related("user").annotate(
            replies_count=Count("replies")
        )
        paginator = ReplyPagination()
        page = paginator.paginate_queryset(replies_qs, request)
        serializer = ListCommentSerializer(
            page, many=True, context={"request": request}
        )
        return paginator.get_paginated_response(serializer.data)
