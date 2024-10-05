import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'comments_spa.settings')
django.setup()

import jwt

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware

from user.models import User
from django.db import close_old_connections

ALGORITHM = "HS256"


@database_sync_to_async
def get_user(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=ALGORITHM)
        print("payload", payload)
    except jwt.ExpiredSignatureError:
        print("Token expired")
        return AnonymousUser()
    except jwt.InvalidTokenError:
        print("Invalid token")
        return AnonymousUser()
    except Exception as e:
        print("Token decode error:", str(e))
        return AnonymousUser()

    try:
        user = User.objects.get(id=payload["user_id"])
        print("user", user)
    except User.DoesNotExist:
        print("User does not exist")
        return AnonymousUser()

    return user


class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        close_old_connections()
        try:
            query_string = scope["query_string"].decode()
            params = dict(x.split("=") for x in query_string.split("&") if "=" in x)
            token_key = params.get("token", None)
        except Exception as e:
            print("Error parsing query string:", str(e))
            token_key = None

        scope["user"] = await get_user(token_key)
        return await super().__call__(scope, receive, send)

def JwtAuthMiddlewareStack(inner):
    return TokenAuthMiddleware(inner)
