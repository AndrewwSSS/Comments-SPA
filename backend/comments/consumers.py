import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache
from asgiref.sync import sync_to_async

from .models import Comment
from .serializers import CommentSerializer


class CommentConsumer(
    AsyncWebsocketConsumer
):
    async def connect(self):
        self.room_name = "chat_room"
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.send(text_data=json.dumps({
            "action": "disconnect",
            "error": "token expired",
        }))
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def get_comments(self):
        cached_comments = await sync_to_async(cache.get)("comments_list")
        if cached_comments:
            return cached_comments
        else:
            comments = await self.get_comments_from_db()
            await sync_to_async(cache.set)("comments_list", comments, timeout=300)
            return comments

    @database_sync_to_async
    def get_comments_from_db(self):
        return CommentSerializer(
            Comment.objects.filter(parent_message=None),
            many=True,
        ).data

    async def send_comments_list(self):
        await self.send(text_data=json.dumps({
            "action": "list_comments",
            "comments": await self.get_comments(),
        }))

    async def receive(self, text_data=None, bytes_data=None):
        if not text_data:
            return

        data = json.loads(text_data)
        text = data.get("content")
        action = data.get("action")
        if action == "create_comment":
            await self.create_comment(text)
            await self.channel_layer.group_send(
                self.room_name,
                {
                    "type": "broadcast_comments"
                }
            )

    async def create_comment(self, text):
        user = self.scope["user"]

        if not user.is_authenticated:
            await self.disconnect(401)
            return

        await self.create_comment_in_db(user, text)

    @database_sync_to_async
    def create_comment_in_db(self, user, text):
        user = Comment.objects.create(
            user=user,
            content=text,
        )
        print(user)
        return user

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "action": "chat_message",
            "comment": event["comment"],
        }))
