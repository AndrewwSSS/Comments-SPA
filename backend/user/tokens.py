from typing import Any

from itsdangerous import (
    URLSafeTimedSerializer,
    BadSignature,
    SignatureExpired
)

from django.conf import settings
serializer = URLSafeTimedSerializer(settings.SECRET_KEY)


def generate_email_verification_token(payload: Any) -> str:
    return serializer.dumps(payload, salt=settings.EMAIL_TOKEN_SALT)


def verify_verification_token(token: str) -> dict | None:
    try:
        return serializer.loads(
            token,
            salt=settings.EMAIL_TOKEN_SALT,
        )
    except (BadSignature, SignatureExpired):
        return None
