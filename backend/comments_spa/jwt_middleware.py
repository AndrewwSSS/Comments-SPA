import os
import jwt
from urllib.parse import parse_qs

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "comments_spa.settings")
django.setup()

from django.contrib.auth import get_user_model
from jwt.exceptions import ExpiredSignatureError
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware

from user.models import User
from django.db import close_old_connections


@database_sync_to_async
def get_user_from_token(token):
    user_model = get_user_model()
    try:
        UntypedToken(token)
        decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = decoded_data.get("user_id")
        return user_model.objects.get(id=user_id)
    except (InvalidToken, TokenError, user_model.DoesNotExist, ExpiredSignatureError):
        return AnonymousUser()


class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = parse_qs(scope["query_string"].decode())
        token = query_string.get("token")
        
        if token:
            user = await get_user_from_token(token[0])
            scope["user"] = user
            if user.is_anonymous:
                await send({
                    "type": "websocket.close",
                    "code": 4001 
                })
                return
        else:
            await send({
                "type": "websocket.close",
                "code": 4003
            })
            return

        return await super().__call__(scope, receive, send)
