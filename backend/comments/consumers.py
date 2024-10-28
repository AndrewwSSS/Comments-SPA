import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache
from asgiref.sync import sync_to_async

from comments.models import Comment
from comments.serializers import CommentSerializer


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

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "action": "chat_message",
            "comment": event["comment"],
        }))
